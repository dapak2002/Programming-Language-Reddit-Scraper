import praw
import string
import csv

# Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET with your Reddit API key and secret
reddit = praw.Reddit(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET", user_agent="my_user_agent")

subreddit_names = ["java" , "typescript", "javascript", "php" , "ruby" , "python", "golang" , "csharp" , "cpp" , "c_programming"]  # List of subreddit names to process

for subreddit_name in subreddit_names:
    subreddit = reddit.subreddit(subreddit_name)  # Get the subreddit

    top_posts = subreddit.hot(limit=100)  # Get the top 100 posts in the subreddit

    frequency = {}  # Dictionary to store the frequency of each word

    for post in top_posts:
        # Get the text of the post
        text = post.title + " " + post.selftext

        # Split the text into words and remove punctuation
        words = text.split()
        words = [word.lower().translate(str.maketrans('', '', string.punctuation)) for word in words]

        # Count the frequency of each word
        for word in words:
            if len(word) >= 4:  # Only consider words with at least 4 characters
                if word in frequency:
                    frequency[word] += 1
                else:
                    frequency[word] = 1

    # Remove certain words from the frequency dictionary
    stop_words = [ "tried" , "instead" , "really" , "something" , "should" , "make" , "been" , "help" , "other" , "please" , "here" , "which" , "using" , "about" , "into" , "know" , "where" , "like", "when" , "only" , "also" , "used" , "there" , "golang" , "python" , "string" , "this", "have" , "with" , "your", "want", "that" , "need" , "just", "will" ,"from" , "some" , "within" , "does" , "would", "what" , "more" , "java" , "typescript", "javascript", "php" , "ruby" , "python", "golang" , "csharp" , "cpp" , "c_programming"]  # Add any other words you want to remove
    for word in stop_words:
        if word in frequency:
            del frequency[word]

    # Sort the frequency dictionary in descending order
    sorted_frequency = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

    # Print the top 10 words with their frequency, preceded by the subreddit name
    print(f"Top words in /r/{subreddit_name}:")
    for i in range(10):
        word, frequency = sorted_frequency[i]
        print(f"{word}: {frequency}")
    print()  # Print an empty line to separate the output for different subreddits

    # Write the words and frequencies to a CSV file
    with open(f"{subreddit_name}.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["word", "frequency"])  # Write the header row
        for word, frequency in sorted_frequency:
            writer.writerow([word, frequency])
