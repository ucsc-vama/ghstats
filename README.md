Using `ghstats`, you can scrape (and accumulate) your repos' download statistics to go beyond GitHub's two-week limit. This repo was inspired by [GitHub-Clone-Scraper](https://github.com/jackwadden/GitHub-Clone-Scraper), and improves upon it by using python3, access tokens (no raw passwords), and JSON. When scraping statistics, ghstats will attempt to merge it with previously downloaded data. Although GitHub provides you the last two weeks of data at a given time, we recommend running ghstats every day with a cron job.

To use ghstats, create a configuration file and provide it as the command line argument:

    $ python3 ghstats.py config.json

Your configuration file should include

* `base_dir` - path to directory to store data
* `username` - username to get access to stats
* `token` - [GitHub Access Token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line) to get permission
* `repo` - array of repos to track, for each repo:
  * `org` - organization name or username for repo (whatever comes before repo's name in URL)
  * `repo` - name of repo
* Peek at `example.json` for an example
