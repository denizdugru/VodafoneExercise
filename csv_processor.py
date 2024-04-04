SPECIAL_CHARACTER_LIST = [
    "@",
    ".",
    ",",
    "-",
    "/",
    " ",
    "_",
]

MASKING_CHARACTER = "X"


class CsvProcessorBase:
    def __init__(self) -> None:
        """
        Initialize CsvProcessorBase.

        Sets data and header_list attributes to empty lists.
        """
        self.data = []
        self.header_list = []

    def load_csv(self, input_file: str, delimiter=",") -> None:
        """
        Load CSV file into memory.

        Args:
            input_file (str): The file path of the input CSV file.
        """
        with open(input_file, mode="r") as file:
            for line_num, line in enumerate(file, start=1):
                if line_num == 1:
                    self.header_list = line.strip().split(delimiter)
                else:
                    values = line.strip().split(delimiter)
                    row_dict = {}
                    for i, value in enumerate(values):
                        row_dict[self.header_list[i]] = value
                    self.data.append(row_dict)

    def encode(self, input_file: str, output_file: str) -> None:
        """
        Encode sensitive data in the CSV file.

        Args:
            input_file (str): The file path of the input CSV file.
            output_file (str): The file path of the output CSV file.
        """
        raise NotImplementedError("The encode method must be implemented in subclass.")


class CsvProcessor(CsvProcessorBase):
    def __init__(self) -> None:
        """
        Initialize CsvProcessor.

        Calls the __init__ method of the base class.
        """
        super().__init__()

    def encode(
        self, input_file: str, output_file: str, mode: str = "character_matching"
    ) -> None:
        """
        Encode sensitive data in the CSV file.

        Args:
            input_file (str): The file path of the input CSV file.
            output_file (str): The file path of the output CSV file.
            mode (str, optional): The mode of encoding. Defaults to "character_matching".
        """
        self.load_csv(input_file)
        self.mask_sensitive_data(mode=mode)
        self.create_output_csv(output_file)

    def mask_sensitive_data(self, mode: str) -> None:
        """
        Mask sensitive data in the CSV file.

        Args:
            mode (str): The mode of masking.
        """
        encoder_func = getattr(self, f"_mask_mode_{mode}")
        name_lengths = [len(row["Name"].replace(" ", "")) for row in self.data]
        billing_values = [
            float(row["Billing"])
            for row in self.data
            if row["Billing"].replace(".", "").isdigit()
        ]
        _ = self.calculate_and_display_stats("Name", name_lengths)
        billing_stats = self.calculate_and_display_stats("Billing", billing_values)

        for row in self.data:
            for key, value in row.items():
                if key in ["Name", "Email"]:
                    masked_value = encoder_func(value, MASKING_CHARACTER)
                    row[key] = masked_value
                elif key == "Billing" and value.replace(".", "").isdigit():
                    row[key] = "{:.1f}".format(billing_stats[2])

    def create_output_csv(self, output_file: str, delimiter=",") -> None:
        """
        Create a new CSV file with masked data.

        Args:
            output_file (str): The file path of the output CSV file.
        """
        with open(output_file, mode="w", newline="") as file:
            file.write(delimiter.join(self.header_list) + "\n")
            for row in self.data:
                row_str = delimiter.join([str(row[key]) for key in self.header_list])
                file.write(row_str + "\n")

    @staticmethod
    def calculate_and_display_stats(column_name: str, values: list) -> tuple:
        """
        Calculate and display statistics for a given column.

        Args:
            column_name (str): The name of the column.
            values (list): The list of values for the column.

        Returns:
            tuple: A tuple containing the maximum, minimum, and average values.
        """
        max_values = round(max(values) if values else 0, 2)
        min_values = round(min(values) if values else 0, 2)
        average_values = round(sum(values) / len(values) if values else 0, 1)

        print(
            f"{column_name}: Max. {max_values}, Min. {min_values}, Avg. {average_values}"
        )

        return max_values, min_values, average_values

    def _mask_mode_character_matching(self, value: str, masking_character: str) -> str:
        """
        Mask characters in the input string based on the masking character.

        Args:
            value (str): The input string to be masked.
            masking_character (str): The character to use for masking.

        Returns:
            str: The masked string.
        """
        return "".join(
            [
                masking_character if char not in SPECIAL_CHARACTER_LIST else char
                for char in value
            ]
        )


if __name__ == "__main__":
    processor = CsvProcessor()
    processor.encode(
        input_file="assets/customers 2.csv",
        output_file="assets/masked_clients.csv",
        mode="character_matching",
    )
