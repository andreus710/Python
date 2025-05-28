
for i in range(1, 20):
    alpha = input("Enter a string: ")
    alpha = alpha.replace(" ", "-")
    alpha = alpha.replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace('/', "").replace(";", "").replace(":", "").replace("!", "").replace("?", "")
    print("The string is: ", alpha)