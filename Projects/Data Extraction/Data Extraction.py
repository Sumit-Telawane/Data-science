import pandas as pd
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Function to extract text from the given URL
def extract_text_from_url(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract article title
        title = soup.title.text if soup.title else ""

        # Extract article text
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.text for p in paragraphs])

        return title, article_text
    except Exception as e:
        print(f"Error extracting text from {url}: {str(e)}")
        return "", ""

# Function to perform text analysis and compute variables
def perform_text_analysis(text):
    # Tokenize the text into sentences and words
    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    # Calculate variables as per the requirements
    word_count = len(words)
    sentence_count = len(sentences)
    avg_sentence_length = word_count / sentence_count

    # Calculate POSITIVE SCORE and NEGATIVE SCORE using TextBlob
    blob = TextBlob(text)
    positive_score = blob.sentiment.polarity
    negative_score = blob.sentiment.subjectivity

    # Calculate POLARITY SCORE and SUBJECTIVITY SCORE
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity

    # Calculate PERCENTAGE OF COMPLEX WORDS
    stop_words = set(stopwords.words('english'))
    complex_words = [word for word in words if word.lower() not in stop_words]
    percentage_complex_words = (len(complex_words) / word_count) * 100

    # Calculate FOG INDEX
    avg_sentence_length_over_3_words = len([s for s in sentences if len(word_tokenize(s)) > 3])
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    # Calculate AVG NUMBER OF WORDS PER SENTENCE
    avg_words_per_sentence = word_count / sentence_count

    # Calculate COMPLEX WORD COUNT
    complex_word_count = len(complex_words)

    # Calculate SYLLABLE PER WORD (Note: A simple count of vowels is used as an approximation)
    syllable_per_word = sum([len(re.findall('(?!e$)[aeiouy]+', word.lower())) for word in words]) / word_count

    # Calculate PERSONAL PRONOUNS (Note: A simple count of personal pronouns is used)
    personal_pronouns = sum([1 for word, pos in pos_tag(words) if pos == 'PRP'])

    # Calculate AVG WORD LENGTH
    avg_word_length = sum([len(word) for word in words]) / word_count

    return positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length, \
           percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count, \
           syllable_per_word, personal_pronouns, avg_word_length

# Read input data from an Excel file
input_file_path = 'input.xlsx'  # Replace with your actual file path
input_data = pd.read_excel(input_file_path)

# Process each URL and perform text analysis
all_results = []  # List to store all analysis results

for index, row in input_data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    # Extract text from the URL
    title, article_text = extract_text_from_url(url)

    # Perform text analysis
    if article_text:
        analysis_results = perform_text_analysis(article_text)

        # Append the analysis results to the list
        all_results.append({
            'URL_ID': url_id,
            'POSITIVE SCORE': analysis_results[0],
            'NEGATIVE SCORE': analysis_results[1],
            'POLARITY SCORE': analysis_results[2],
            'SUBJECTIVITY SCORE': analysis_results[3],
            'AVG SENTENCE LENGTH': analysis_results[4],
            'PERCENTAGE OF COMPLEX WORDS': analysis_results[5],
            'FOG INDEX': analysis_results[6],
            'AVG NUMBER OF WORDS PER SENTENCE': analysis_results[7],
            'COMPLEX WORD COUNT': analysis_results[8],
            'WORD COUNT': analysis_results[9],
            'SYLLABLE PER WORD': analysis_results[10],
            'PERSONAL PRONOUNS': analysis_results[11],
            'AVG WORD LENGTH': analysis_results[12],
        })

# Create a DataFrame with all analysis results
all_results_df = pd.DataFrame(all_results)

# Save all results to a single Excel file
output_file_name = 'All_Results.xlsx'
all_results_df.to_excel(output_file_name, index=False)
