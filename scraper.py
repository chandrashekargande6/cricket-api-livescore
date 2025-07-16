import requests
from bs4 import BeautifulSoup

def get_match_scorecard(match_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(match_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    match_data = {
        "team_scores": [],
        "players": []
    }

    try:
        # Team scores
        score_blocks = soup.find_all("div", class_="cb-col cb-col-100 cb-scrd-hdr-rw")
        for block in score_blocks:
            text = block.get_text(separator=' ', strip=True)
            if text:
                match_data["team_scores"].append(text)

        # Batting players
        innings = soup.find_all("div", class_="cb-col cb-col-100 cb-ltst-wgt-hdr")
        for inning in innings:
            rows = inning.find_all("div", class_="cb-col cb-col-100 cb-scrd-itms")
            for row in rows:
                cols = row.find_all("div")
                if len(cols) >= 4:
                    name = cols[0].text.strip()
                    runs = cols[2].text.strip()
                    balls = cols[3].text.strip()
                    if name and name.lower() != "extras" and runs.isdigit():
                        match_data["players"].append({
                            "name": name,
                            "runs": runs,
                            "balls": balls
                        })

    except Exception as e:
        match_data["error"] = str(e)

    return match_data


def get_all_live_matches():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    matches = []

    match_blocks = soup.find_all("div", class_="cb-mtch-lst cb-col cb-col-100 cb-tms-itm")

    for block in match_blocks:
        try:
            title = block.find("a", class_="text-hvr-underline").text.strip()
            partial_link = block.find("a")["href"]
            original_link = "https://www.cricbuzz.com" + partial_link
            scorecard_link = original_link.replace("live-cricket-scores", "live-cricket-scorecard")

            status = block.find("div", class_="cb-text-live").text.strip() \
                if block.find("div", class_="cb-text-live") else (
                block.find("div", class_="cb-text-complete").text.strip()
                if block.find("div", class_="cb-text-complete") else "Status Unknown")

            # Fetch scorecard and players
            match_details = get_match_scorecard(scorecard_link)

            matches.append({
                "title": title,
                "status": status,
                "link": original_link,
                "team_scores": match_details.get("team_scores", []),
                "players": match_details.get("players", [])
            })
        except Exception as e:
            matches.append({"error": str(e)})

    return matches
