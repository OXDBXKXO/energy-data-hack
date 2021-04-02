def write_data_to_output(data, file_path = None):
    if file_path is None:
        for k in data:
            print(k)

    else:
        with open(file_path, "w") as file:
            for k in data:
                file.write(k)
                file.write('\n')
