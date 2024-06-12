# Adobe Popup Remover

As mentioned [here](https://www.reddit.com/r/GenP/wiki/redditgenpguides/#wiki_.28....29_troubleshoot_section_.7C_unlicensed_popup), to remove the unlicensed popup, you need to block certain domains that Adobe uses to check your license. This script will automate that process for you.

## How to Run

This script will edit your `C:\Windows\System32\drivers\etc\hosts` file, so it needs to be run as an administrator. The process is simple:

1. Open `cmd` as an administrator.
2. Navigate to the directory containing the script:
   `cd "path to the python script"`
3. Run the script:
  `python main.py`
4. Wait for the message:
 `Ok you can close the script now...`

# Can I Run It Again if the Popup Appears?
Yes, you can run it again. The script will not overwrite anything in your hosts file nor will it write new data without removing the old entries. It will fetch the data from the endpoint and replace the old entries with the new ones.

# More to Know

This script will only block on `0.0.0.0`. 

# Credits
The list that the script fetches is from:
https://a.dove.isdumb.one/list.txt
\
Method from:
[/r/GenP](https://www.reddit.com/r/GenP/wiki/redditgenpguides/#wiki_.28....29_troubleshoot_section_.7C_unlicensed_popup)

# ~
Kindly leave a star if you find this helpful and would like to support the project.
