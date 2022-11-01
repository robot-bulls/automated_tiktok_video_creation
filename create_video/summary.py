import openai
from create_video.edittext import isfloat
import traceback

def summarize(content, language):

    if language == "en":
        command = "Summarize this for a fifth-grade student in a thrilling way in five sentences:\n\n"
    elif language == "de":
        command = "Fasse das für einen Fünftklässler in fünf Sätzen auf spannende Weise zusammen:\n\n"
    elif language == "fr":
        command = "Résume cela de manière captivante en cinq phrases pour un élève de cinquième année:\n\n"
    elif language == "it":
        command = "Fate un riassunto per un bambino di quinta elementare in cinque frasi e in modo appassionante:\n\n"

    tldr_tag = "\n tl;dr:"
    grader_tag = command
    openai.organization = ''
    openai.api_key = "XXXXX"

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=grader_tag + content,
        temperature=0.6,
        max_tokens=447,
        top_p=0.51,
        best_of=3,
        frequency_penalty=0.5,
        presence_penalty=0
    )

    summary = response["choices"][0]["text"]
    # replace long numbers with rounded number
    for word in summary.split():  
        try:
            if isfloat(word) and not any(p in word for p in "!#$%&(*+ -/:;<=>?@[\]^_{|~") and not any(c.isalpha() for c in word):
                initial_word = word
                word = word.replace(".", "")
                word = word.replace(",", ".")
                if float(word) <= 5:
                    x = round(float(word), 2)
                elif float(word) > 5:
                    x = round(
                        float(word), ((len(str(round(float(word))))*-1)+1))
                    x = round(x)
                # print("i: ", str(initial_word), "a: ", str(x))
                summary = summary.replace(initial_word, str(x))
        except Exception as e:
            print(traceback.format_exc())

    # return response["choices"][0]["text"]
    return summary
