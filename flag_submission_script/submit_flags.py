import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urlparse, parse_qs


def parse_link(link):
    parsed_url = urlparse(link)
    query_params = parse_qs(parsed_url.query)
    team_id = query_params.get('team_id', [''])[0]
    flag_id = query_params.get('flag_id', [''])[0]
    return team_id, flag_id

def submit_flag(team_number, flag_number, flag_data, reason):
    csrftoken = ''
    sessionid = ''
    csrfmiddlewaretoken = ''

    cookies = {
    'csrftoken': csrftoken,
    'sessionid': sessionid,
}

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://iscore.iseage.org',
        'Connection': 'keep-alive',
        'Referer': 'https://iscore.iseage.org/red/flag/capture/?team_id=386&flag_id=557',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
    }

    params = {
        'team_id': team_number,
        'flag_id': flag_number,
    }

    data = {
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'team': team_number,
        'flag': flag_number,
        'data': flag_data,
        'notes': reason,
        'Submit': 'Submit',
    }

    response = requests.post('https://iscore.iseage.org/red/flag/capture/', params=params, cookies=cookies, headers=headers, data=data)
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        div_tag = soup.find('div', class_='notifications top-center')
        result  = div_tag['data-row']
        print(result)
    except:
        #print(response.text)
        pass
    print(f"submitted with reason: {reason}")
    

def print_flag_data(flag, reason):
    csrftoken = ''
    sessionid = ''
    csrfmiddlewaretoken = ''


    cookies = {
        'csrftoken': csrftoken ,
        'sessionid': sessionid ,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://iscore.iseage.org/red/flag/lookup/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://iscore.iseage.org',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = {
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'flag': flag,
        'Submit': 'Submit',
    }

    response = requests.post('https://iscore.iseage.org/red/flag/lookup/', cookies=cookies, headers=headers, data=data)
    if "login" in response.text or "Login" in response.text or "Forbidden" in response.text:
        print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    dl_tags = soup.find_all('dl')
    dt_dd_pairings=[]
    for dl in dl_tags:
        # Extract the content within <dl> tags
        for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
            dt_dd_pairings.append({"dt" : dt, "dd" : dd})
            #print(dt.text.strip(), ":", dd.text.strip())
    if len(dt_dd_pairings) > 0:
        print(flag)
    for pairing in dt_dd_pairings:
        if "Action" in pairing['dt'].text.strip():
            link = "https://iscore.iseage.org" + pairing["dd"].find('a')['href']
            team_id, flag_id = parse_link(link)
            submit_flag(team_id, flag_id, flag, reason)

            print(link)
        else:
            print(pairing['dt'].text.strip(), ":", pairing["dd"].text.strip())

def main():
    parser = argparse.ArgumentParser(description="Read and print each line from a file.")
    parser.add_argument("filename", help="Name of the file to read")
    parser.add_argument('--reason', type=str, required=True, help='Specify the reason')
    args = parser.parse_args()
    reason = args.reason
    with open(args.filename, 'r') as file:
        for line in file:
            print_flag_data(line.strip(), reason)

if __name__ == "__main__":
    main()
