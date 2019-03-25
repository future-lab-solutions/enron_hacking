import re
import pandas as pd

def get_emails_from_csv(filepath):
    """Converts csv of emails into Dataframe of emails.

    Takes in the email dataset which is in csv form and
    converts it into a pandas dataframe.

    Args:
        filepath: The email csv filepath.

    Returns:
        A pandas Dataframe with two columns, "file" and
        "message".
    """
    email_dataframe = pd.read_csv(filepath)
    return email_dataframe


def get_email_keys(email_dataframe,sample_count):
    """Returns a list of keys found in the emails.

    Keys are not consistent across all emails in the 
    dataframe. This function goes through a specified 
    number of emails from the dataframe of emails and 
    creates a list of all keys found in those emails.

    Args:
        email_dataframe: Dataframe of all emails from
        dataset.
        sample_count: Number of emails to create list
        of keys from. 

    Return:
        A set of all keys found in sample_count
        number of emails.
    """
    sampled_emails = email_dataframe.message.sample(sample_count)
    allkeys = [re.findall('\n([\w\-]+):', email[:email.find('\n\n')]) for email in sampled_emails]
    allkeys = sum(allkeys,[])
    allkeys.append('Message-ID')
    allkeys=list(dict.fromkeys(allkeys))
    return allkeys

def make_list_of_email_dicts(email_dataframe,allkeys, number_of_emails):
    """Returns a list of parsed emails.

    Loops through number of emails in the dataset and 
    converts them into a dictionary, and appends 
    dictionary to a list.

    Args:
        email_dataframe: Dataframe of emails from 
        dataset.
        allkeys: Dictionary of keys found in the
        email dataset.
        number_of_emails: Number of emails to loop
        through

    Return:
        A list of dictionaries of each email.
    """
    list_of_email_dicts = []
    i = 0
    for email in email_dataframe.message:

        email_dicts = {}
        for key in allkeys:
            try:
                email_dicts[key] = email[email.index(key)+len(key)+1:email.find('\n',email.index(key))].strip() 
            except:
                email_dicts[key] = ''

        email_dicts['Body'] = email[email.find('\n\n'):].strip()
        list_of_email_dicts.append(email_dicts)

        i = i + 1

        if i % 200 == 0:
            print('Completed ' + str(i) + ' emails')

        if i % number_of_emails == 0:
            break

    return list_of_email_dicts


if __name__ == "__main__":
    email_dataframe = get_emails_from_csv('data/emails.csv')
    allkeys = get_email_keys(email_dataframe,1000)
    list_of_email_dicts = make_list_of_email_dicts(email_dataframe,allkeys,100000)



