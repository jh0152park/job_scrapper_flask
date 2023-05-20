import os
import save
import extractor
from flask import *

DB = {}



def main():
    app = Flask("JobScrapper")

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/search")
    def search():
        global DB
        
        skill = request.args.get("skill")
        if not skill:
            return redirect("/")
        
        if skill not in DB:
            jobs = extractor.get_remoteok_jobs(skill) + extractor.get_wwr_jobs(skill)
            DB[skill] = jobs
        else:
            jobs = DB[skill]
        save.create_csv(skill, jobs)
        return render_template("search.html", skill=skill, jobs=jobs, jobs_count=len(jobs))
    
    @app.route("/export")
    def export():
        global DB
        
        skill = request.args.get("skill")
        if not skill:
            return redirect("/")
        if skill not in DB:
            return redirect(f"/search?skill={skill}")
        return send_file(f"{skill}_search_result.csv", as_attachment=True)


    app.run("0.0.0.0")

if __name__ == "__main__":
    main()