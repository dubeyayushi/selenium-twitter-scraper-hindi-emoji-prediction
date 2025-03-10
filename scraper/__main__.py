import os
import sys
import argparse
import getpass
import csv
from twitter_scraper import Twitter_Scraper

try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)


def scrape_usernames_from_csv(csv_path):
    """
    Read usernames from a CSV file.
    
    Args:
        csv_path (str): Path to the CSV file containing usernames.
    
    Returns:
        list: List of usernames extracted from the CSV file.
    """
    usernames = []
    try:
        with open(csv_path, 'r') as csvfile:
            # Assume the first column contains usernames
            reader = csv.reader(csvfile)
            # Skip header if exists
            next(reader, None)
            usernames = [row[0].strip() for row in reader if row]
        return usernames
    except FileNotFoundError:
        print(f"Error: CSV file {csv_path} not found.")
        sys.exit(1)
    except IndexError:
        print(f"Error: CSV file {csv_path} appears to be empty or improperly formatted.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)


def main():
    try:
        parser = argparse.ArgumentParser(
            add_help=True,
            usage="python scraper [option] ... [arg] ...",
            description="Twitter Scraper is a tool that allows you to scrape tweets from twitter without using Twitter's API.",
        )

        try:
            parser.add_argument(
                "--mail",
                type=str,
                default=os.getenv("TWITTER_MAIL"),
                help="Your Twitter mail.",
            )

            parser.add_argument(
                "--user",
                type=str,
                default=os.getenv("TWITTER_USERNAME"),
                help="Your Twitter username.",
            )

            parser.add_argument(
                "--password",
                type=str,
                default=os.getenv("TWITTER_PASSWORD"),
                help="Your Twitter password.",
            )
        except Exception as e:
            print(f"Error retrieving environment variables: {e}")
            sys.exit(1)

        parser.add_argument(
            "-t",
            "--tweets",
            type=int,
            default=50,
            help="Number of tweets to scrape per username (default: 50)",
        )

        parser.add_argument(
            "-u",
            "--username",
            type=str,
            default=None,
            help="Twitter username. Scrape tweets from a user's profile.",
        )

        parser.add_argument(
            "--usernames-csv",
            type=str,
            default=None,
            help="Path to a CSV file containing usernames to scrape. First column should contain usernames.",
        )

        parser.add_argument(
            "-ht",
            "--hashtag",
            type=str,
            default=None,
            help="Twitter hashtag. Scrape tweets from a hashtag.",
        )

        parser.add_argument(
            "-ntl",
            "--no_tweets_limit",
            nargs='?',
            default=False,
            help="Set no limit to the number of tweets to scrape (will scrap until no more tweets are available).",
        )

        parser.add_argument(
            "-q",
            "--query",
            type=str,
            default=None,
            help="Twitter query or search. Scrape tweets from a query or search.",
        )

        parser.add_argument(
            "-a",
            "--add",
            type=str,
            default="",
            help="Additional data to scrape and save in the .csv file.",
        )

        parser.add_argument(
            "--latest",
            action="store_true",
            help="Scrape latest tweets",
        )

        parser.add_argument(
            "--top",
            action="store_true",
            help="Scrape top tweets",
        )

        parser.add_argument(
            "--language",
            type=str,
            default="en",  # Default to English if not provided
            help="Language of tweets to scrape (default: en). Use 'hi' for Hindi, 'en' for English, 'hien' for Hinglish etc.",
        )

        args = parser.parse_args()

        USER_MAIL = args.mail
        USER_UNAME = args.user
        USER_PASSWORD = args.password

        if USER_UNAME is None:
            USER_UNAME = input("Twitter Username: ")

        if USER_PASSWORD is None:
            USER_PASSWORD = getpass.getpass("Enter Password: ")

        print()

        # Check for conflicting arguments
        tweet_type_args = []
        if args.username is not None:
            tweet_type_args.append(args.username)
        if args.hashtag is not None:
            tweet_type_args.append(args.hashtag)
        if args.query is not None:
            tweet_type_args.append(args.query)
        if args.usernames_csv is not None:
            tweet_type_args.append(args.usernames_csv)

        additional_data: list = args.add.split(",")

        if len(tweet_type_args) > 1:
            print("Please specify only one of --username, --hashtag, --query, or --usernames-csv.")
            sys.exit(1)

        if args.latest and args.top:
            print("Please specify either --latest or --top. Not both.")
            sys.exit(1)

        # Determine usernames to scrape
        usernames_to_scrape = []
        if args.username:
            usernames_to_scrape = [args.username]
        elif args.usernames_csv:
            usernames_to_scrape = scrape_usernames_from_csv(args.usernames_csv)

        if USER_UNAME is not None and USER_PASSWORD is not None:
            scraper = Twitter_Scraper(
                mail=USER_MAIL,
                username=USER_UNAME,
                password=USER_PASSWORD,
                language=args.language,
            )
            scraper.login()

            # Scrape for each username
            for username in usernames_to_scrape:
                print(f"\nScraping tweets for username: {username}")
                scraper.scrape_tweets(
                    max_tweets=args.tweets,
                    no_tweets_limit=args.no_tweets_limit if args.no_tweets_limit is not None else True,
                    scrape_username=username,
                    scrape_hashtag=args.hashtag,
                    scrape_query=args.query,
                    scrape_latest=args.latest,
                    scrape_top=args.top,
                    scrape_poster_details="pd" in additional_data,
                )
                scraper.save_to_csv()

            if not scraper.interrupted:
                scraper.driver.close()
        else:
            print(
                "Missing Twitter username or password environment variables. Please check your .env file."
            )
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nScript Interrupted by user. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()