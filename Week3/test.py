import numpy as np

# Creating a matrix
matrix_A = np.array([[1, 2], [3, 4]])
print("Matrix A:\n", matrix_A)

# Reshaping a matrix
reshaped_matrix = np.reshape(matrix_A, (4, 1))
print("Reshaped Matrix:\n", reshaped_matrix)

# Changing values in a matrix
matrix_A[0, 0] = 5
print("Updated Matrix A:\n", matrix_A)

# Example survey data matrix (5 respondents, 4 questions)
survey_data = np.array([[5, 1, 4, 4],
                        [4, 2, 4, 3],
                        [5, 1, 1, 5],
                        [3, 2, 1, 2],
                        [2, 1, 2, 5]])



# Calculating various statistics
average_responses = np.mean(survey_data, axis=0)
total_responses = np.sum(survey_data, axis=0)
max_responses = np.max(survey_data, axis=0)
min_responses = np.min(survey_data, axis=0)

print("Average Responses:", average_responses)
print("Total Responses:", total_responses)
print("Maximum Responses:", max_responses)
print("Minimum Responses:", min_responses)


# Defining matrices
price_matrix = np.array([[10, 15],
                         [12, 18]])
quantity_matrix = np.array([[30, 40],
                            [25, 35]])

# Multiplying matrices to get total sales
total_sales_matrix = np.dot(price_matrix, quantity_matrix.T)

print("Total Sales Matrix:\n", total_sales_matrix)