JOURNAL_PROMPT = """
    You are an expert at teansforming a raw text into a Series of Sequential events like a journal.
    Your goal is to prepare a journal with the information of the events which happened in the given text.
    You have to preserve all the important events which happened and whatever important information is present in the given text.
    
    Note: transform this text into a single day's journal and write them like a person would write in their diary, but in the form of sequential events

    ------------
    {text}
    ------------

    

    The Journal timeline is
"""