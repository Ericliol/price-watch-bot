tester_input = input("hi tester! input url to get price, input E to exit---  ")
while tester_input != "E":
    print(get_price_single_url(tester_input))
    tester_input = input("hi tester! input url to get price, input E to exit---  ")