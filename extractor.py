import requests
from bs4 import BeautifulSoup

office_default_image = "https://cdn-icons-png.flaticon.com/128/3160/3160762.png"

def get_remoteok_jobs(term="python"):
    url = f"https://remoteok.com/remote-{term}-jobs"
    request = requests.get(url, headers={"User-Agent": "Kimchi"})
    if request.status_code == 200:
        soup = BeautifulSoup(request.text, "html.parser")

        jobs = []
        temp = soup.find_all("tr")
        job_list = [_ for _ in temp if "data-offset" in _.attrs]

        for job in job_list:
            link = "https://remoteok.com/" + job.find("td", attrs={"class": "company position company_and_position"}).a["href"]
            title = job.find("td", attrs={"class": "company position company_and_position"}).a.h2.text.strip()
            office_name = job.find("span", attrs={"itemprop": "hiringOrganization"}).text.strip()
            extra_info = job.find_all("div", attrs={"class": ["location tooltip", "location"]})
            locate = ", ".join(e.text for e in extra_info[:-1])
            pay = extra_info[-1].text
            all_tags = job.find_all("a", attrs={"class": "no-border tooltip-set action-add-tag"})
            tags = ", ".join(t.text.strip() for t in all_tags)
            left_days = job.find("td", attrs={"class": "time"}).time.text.strip()
            image = job.find("td", attrs={"class": "image has-logo"})
            if image:
                image = image.a.img["data-src"]
            else:
                image = office_default_image
            
            
            if title not in jobs:
                jobs.append({
                    "company": office_name,
                    "title": title,
                    "locate": locate,
                    "pay": pay,
                    "tags": tags,
                    "left_days": left_days,
                    "type": "Unknowun",
                    "link": link,
                    "image": image
                })
        return jobs
    else:
        print("Can't get jobs.")

def get_wwr_jobs(job="python"):
    jobs = []
    url = "https://weworkremotely.com/remote-jobs/search?term="

    res = requests.get(url+job)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    companies = soup.find_all("li", attrs={"class": "feature"})

    for company in companies:
        link = company.find_all("a")[1]["href"]
        link = "/".join(url.split("/")[:3]) + "/" + link
        office, work_type, locate = company.find_all("span", attrs={"class": "company"})
        office, work_type, locate = office.text, work_type.text, locate.text
        title = company.find("span", attrs={"class": "title"}).text
        image = company.find("div", class_ = "flag-logo")

        if image:
            image = image["style"].split("background-image:url(")[-1][:-1]
        else:
            image = office_default_image
            

        jobs.append({
            "company": office,
            "link": link,
            "title": title,
            "type": work_type,
            "locate": locate,
            "image": image
        })

    return jobs