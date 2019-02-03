#   Final project (Linear Fit program)
#   The main function "fit_linear" will extracts data points from the input file and plots a linear function into
#   a graph ,according to the data calculations


def fit_linear(filename):
    import matplotlib.pyplot as plt
    import numpy as np

    file_pointer = open(filename, 'r')
    tables_data = file_pointer.readlines()
    list2d_data = []

    for line in tables_data:  # This loop will strip "/n" characters and split the words into lists by whitespace
        line = line.rstrip().split()
        list2d_data += [line]  # list2d_data will be a 2D-list of the lines

    # The function ,dataValidation, checks the data and returns an ordered 2D-list of the data in rows format
    # after testing its validity

    def dataValidation(data):

        # Input Data is in Columns format,function--------------------------

        def dataisCol(data1):
            ordered_cols_list = []
            for d in range(len(data1)):  # adding empty  rows lists according to the data's length
                ordered_cols_list.append([])

            for rows in data1:
                list_index = data1.index(rows)
                for k in range(len(rows)):
                    ordered_cols_list[list_index].append(None)

            flist_len_compare = len(ordered_cols_list[1])
            for rows in ordered_cols_list[2:]:  # check if rows length are the same as the first list of data points
                if len(rows) != flist_len_compare:
                    print("Input file error: Data lists are not the same length.")
                    return

            headers = data1[0]
            titles = ["x", "dx", "y", "dy"]
            for k in range(len(headers)):
                headers[k] = headers[k].lower()  # converting the headers to lower case

            for element in titles:  # ordering the data according to titles indexes
                if element in headers:
                    titles_index = titles.index(element)
                    headers_index = headers.index(element)
                    i = 0
                    while i < len(data1):
                        for list_index in data1:
                            ordered_cols_list[i][titles_index] = list_index[headers_index]
                            i = i + 1

            for rows in ordered_cols_list[1:]:  # conversion of integers/floats strings to floats
                for c in range(len(rows)):
                    rows[c] = float(rows[c])
        
            for rows in ordered_cols_list[1:]:  # testing if uncertainties are greater than zero
                dx_uncertainty = rows[1]
                dy_uncertainty = rows[3]
                if dx_uncertainty < 0 or dy_uncertainty < 0:
                    print("Input file error: Not all uncertainties",
                                                    "are positive.")
                    return
            del ordered_cols_list[0]

            x_col_to_row = []  # creating lists for each type of data
            y_col_to_row = []
            dx_col_to_row = []
            dy_col_to_row = []

            for listx in ordered_cols_list:
                x_col_to_row.append(listx[0])
            for listdx in ordered_cols_list:
                dx_col_to_row.append(listdx[1])

            for listy in ordered_cols_list:
                y_col_to_row.append(listy[2])

            for listdy in ordered_cols_list:
                dy_col_to_row.append(listdy[3])

            new_data_list = []  # creating a list that will contain the data as rows
            new_data_list.append(x_col_to_row)
            new_data_list.append(dx_col_to_row)
            new_data_list.append(y_col_to_row)
            new_data_list.append(dy_col_to_row)

            return new_data_list

        # Input Data is in Rows format,function-----------------------------
         
        def dataisRow(data2):
            ordered_rows_list = []

            for p in range(len(data2)):  # adding empty  rows lists according to the data's length
                ordered_rows_list.append([])

            for rows in data2:  # switching the headers to lower case
                rows[0] = rows[0].lower()

            titles = ["x", "dx", "y", "dy"]
            for list_index in data2:  # reordering the rows according to titles
                headers = list_index[0]

                if headers in titles:
                    titles_index = titles.index(headers)
                    ordered_rows_list[titles_index] = list_index

            for rows in ordered_rows_list:  # conversion of integers/floats strings to floats
                for num_index in range(1, len(rows)):
                    rows[num_index] = float(rows[num_index])

            frow_lencompare = len(ordered_rows_list[0])  # the first row of the data
            for rows in ordered_rows_list[1:]:  # comparing data lists length
                if len(rows) != frow_lencompare:
                    print("Input file error: Data lists are not the same length.")
                    return

            dx_row = ordered_rows_list[1]
            dy_row = ordered_rows_list[3]
            for number in dx_row[1:]:  # the following loops will check uncertainties
                if number < 0:
                    print("Input file error: Not all uncertainties",
                                                    "are positive.")
                    return
            for number in dy_row[1:]:
                if number < 0:
                    print("Input file error: Not all uncertainties",
                                                    "are positive.")
                    return
            for rows in ordered_rows_list:  # deleting the titles for each rows
                del rows[0]

            return ordered_rows_list

        graph_titles = []
        empty_list_index = list2d_data.index([])  # This will find the location of the empty list in the data 2D-list
        for n in range(3):  # This loop will remove the empty list and the graphs titles from the data 2D-list
            graph_titles.append(list2d_data.pop(empty_list_index))
        graph_titles.remove([])

        # This section will check if the data is in rows or columns
        element_test = list2d_data[0][1]
        if element_test.isalpha():  # if element_test is alphabetic, return cols function
            return dataisCol(data), graph_titles
        else:
            return dataisRow(data), graph_titles

    fixed_data, final_graph_titles = dataValidation(list2d_data)

    if fixed_data is None:  # if the data isn't right for linear fit, stop the main function
        return

    del final_graph_titles[0][0:2]
    del final_graph_titles[1][0:2]
    x_title_label = ' '.join(final_graph_titles[0])
    y_title_label = ' '.join(final_graph_titles[1])
    x_data = fixed_data[0]  # fixed_data is a 2D-list that has the data points in rows format
    dx_data = fixed_data[1]
    y_data = fixed_data[2]
    dy_data = fixed_data[3]

    def fittingCalculations(x_data1, dx_data1, y_data1, dy_data1):
        import math

        N = len(y_data1)  # number of points
        z = 0
        x_mean = 0
        y_mean = 0
        xy_mean = 0
        dy_mean2 = 0
        x_mean2 = 0

        for k in range(N):  # calculations of the means
            z += 1/(dy_data1[k]**2)
            x_mean += (x_data1[k]/(dy_data1[k])**2)
            y_mean += (y_data1[k]/(dy_data1[k])**2)
            xy_mean += (x_data1[k]*y_data1[k]/(dy_data1[k])**2)
            dy_mean2 += (dy_data1[k]/dy_data1[k])**2
            x_mean2 += (x_data1[k]/dy_data1[k])**2

        x_final = x_mean/z
        y_final = y_mean/z
        xy_final = xy_mean/z
        dy2_final = dy_mean2/z
        x2_final = x_mean2/z

        a_calc = (xy_final-(x_final*y_final))/(x2_final - x_final**2)
        b_calc = (y_final-a_calc*x_final)
        da_calc = math.sqrt(dy2_final / (N*(x2_final - x_final**2)))
        db_calc = math.sqrt(dy2_final * x2_final / (N*(x2_final - x_final**2)))

        chi2_calc = 0
        for t in range(N):
            chi2_calc += ((y_data1[t]-(a_calc*(x_data1[t])+b_calc)) / dy_data1[t])**2
        chi2_reduced_calc = chi2_calc / (N-2)
        return a_calc, b_calc, da_calc, db_calc, chi2_calc, chi2_reduced_calc

    # printing the fitting calculations results
    a, b, da, db, chi2, chi2_reduced = fittingCalculations(x_data, dx_data, y_data, dy_data)
    print("a = ", a, "+-", da)
    print("b = ", b, "+-", db)
    print("chi2 = ", chi2)
    print("chi2_reduced = ", chi2_reduced)

    # plotting the linear function into a graph
    x_values = np.array(x_data)
    y_values = a*x_values + b
    plt.plot(x_values, y_values, 'r-')
    plt.errorbar(x_data, y_data, yerr=dy_data, xerr=dx_data, fmt='none', ecolor="b")
    plt.ylabel(y_title_label)
    plt.xlabel(x_title_label)
    plt.savefig("linear_fit.svg")
    return
