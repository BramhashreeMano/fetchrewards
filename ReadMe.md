# Coding Assignment

I have implemented the coding exercise using Python, Flask and Flask-RESTful.

## Instructions to run the program:

Clone the repository to the local machine.

In the terminal

1) Create a docker image using the following command: docker build .

2) Copy image_id by executing : docker images

3) To run: docker run -d -p 8080:8080 #paste image_id

4) Once the server is running, the application can be tested in 2 ways:

    i)  Run the test cases using the command: python -m unittest test.py
    
        (which tests the examples provided in the assignment)

    ii) Use Postman to hit the server:

        a) Endpoint: Process Receipts
        POST : http://localhost:8080/receipts/process 
        
        Input:  Pass the Receipt JSON as the Payload
        Output: JSON containing an id for the receipt

        b) Endpoint: Get Points
        GET : http://localhost:8080/receipts/<string:id>/points/   

        Note: Pass the id generated from the previous POST method in the above link instead of "<string:id>"

        Input:  No input is passed 
        Output: A JSON object containing the number of points awarded

Final Comments: The application works, generating the desired output for all examples.
                I have used try-catch blocks to ensure app reliability and have coded in such a way 
                even if parts of the Receipt JSON are missing, the app will still run successfully.






