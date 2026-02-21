import requests

# this script assumes the Flask server from app.py is running on localhost:5000

url = "http://127.0.0.1:5000/admn"

def check_score(score, category="General"):
    data = {"score": score, "category": category}
    resp = requests.post(url, data=data)
    if resp.status_code != 200:
        print(f"ERROR: server returned {resp.status_code}")
        return None
    # the response is HTML; we just print a slice to eyeball the numbers
    text = resp.text
    print(f"POST score={score},category={category} -> response snippet")
    start = text.find("<h2>Results:")
    print(text[start:start+200])

if __name__ == "__main__":
    for score in [70, 80, 90, 100]:
        check_score(score)
