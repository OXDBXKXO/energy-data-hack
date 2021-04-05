def write_data_to_output(data, file_path = None):
    """
        Write the container given as argument.
        Each element is printed on a line.

        Args:
            data:       The data to write. It is treated as a container.

            file_path:  The path of the file in which put the data.
                        If no file name is given, put the string on stdout.

        Examples:
            >>> write_data_to_output(["this", "is", "an", "example"])
            this
            is
            an
            example
    """

    # Print on stdout
    if file_path is None:
        for k in data:
            print(k)

    # Print in a file
    else:
        with open(file_path, "w") as file:
            for k in data:
                file.write(k)
                file.write('\n')
