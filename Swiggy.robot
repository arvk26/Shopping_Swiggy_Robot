*** Settings ***
Library           swiggy.py

*** Test Cases ***
Order-Swiggy
    [Setup]    Launch Browser    https://www.swiggy.com
    Choose Exact Location    Indiranagar, Bengaluru
    Search Restaurent    Bite Me
    Select Items To Order    Red Velvet Cupcake    2
    Select Items To Order    Tiramisu \ Cupcake    1
    Select Items To Order    Irish Coffee Cupcake    1
    Select Items To Order    Choco Choco Cupcake    1
    Checkout And Get All Items On Checkout Page
    Verify Items On Checkout Page    Red Velvet Cupcake    2
    Verify Items On Checkout Page    Tiramisu Cupcake    1
    Verify Items On Checkout Page    Irish Coffee Cupcake    1
    Verify Items On Checkout Page    Choco Choco Cupcake    1
    Signup    0000000000    abc abc    abc@def.com    abcdef
    Verify Email Error And Take Screenshot
    Update Items During Checkout    Red Velvet Cupcake    1
    [Teardown]    swiggy.Close Browser
