from pathlib import Path
import json


class ResumeService:
    def __init__(self):
        self.data_dir = (
            Path(__file__)
            .resolve()
            .parent.parent
            / "data"
        )

        self.profile = self._load_json("candidate_profile.json")
        self.experience = self._load_json("experience.json")
        self.skills = self._load_json("skills_catalog.json")
        self.projects = self._load_json("project_catalog.json")
        self.achievements = self._load_json("achievements.json")

    def _load_json(self, filename: str):
        path = self.data_dir / filename

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------
    # Candidate Profile
    # -----------------------------

    def get_candidate_profile(self):
        return self.profile

    def get_candidate_name(self):
        return self.profile["name"]

    def get_summary(self):
        return self.profile["summary"]

    def get_education(self):
        return self.profile["education"]

    # -----------------------------
    # Experience
    # -----------------------------

    def get_experience(self):
        return self.experience["experience"]

    def get_latest_experience(self):
        experiences = self.experience["experience"]

        if not experiences:
            return None

        return experiences[0]

    # -----------------------------
    # Skills
    # -----------------------------

    def get_all_skills(self):
        return self.skills

    def get_flattened_skills(self):
        skills = []

        for category in self.skills.values():
            skills.extend(category)

        return list(set(skills))

    # -----------------------------
    # Projects
    # -----------------------------

    def get_projects(self):
        return self.projects["projects"]

    def get_project_by_id(self, project_id):
        for project in self.projects["projects"]:
            if project["id"] == project_id:
                return project

        return None

    def get_project_by_name(self, project_name):
        for project in self.projects["projects"]:
            if project["name"].lower() == project_name.lower():
                return project

        return None

    # -----------------------------
    # Achievements
    # -----------------------------

    def get_achievements(self):
        return self.achievements["achievements"]

    # -----------------------------
    # Agent Helper Methods
    # -----------------------------

    def get_candidate_context(self):
        """
        Full candidate profile for LLMs.
        """

        return {
            "profile": self.profile,
            "experience": self.experience,
            "skills": self.skills,
            "projects": self.projects,
            "achievements": self.achievements
        }

    def get_project_summaries(self):
        """
        Lightweight project info for matching.
        """

        return [
            {
                "id": project["id"],
                "name": project["name"],
                "category": project["category"],
                "skills": project["skills"],
                "keywords": project["keywords"],
                "priority": project["priority"]
            }
            for project in self.projects["projects"]
        ]
    
    def get_projects_by_skill(self, skill: str):
        matches = []

        for project in self.projects["projects"]:

            project_skills = [
                s.lower()
                for s in project["skills"]
            ]

            if skill.lower() in project_skills:
                matches.append(project)

        return matches