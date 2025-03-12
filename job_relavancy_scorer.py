from job_posting_scraper_ai import get_scraped_job_data
from db_manager import get_employment, get_job_postings
import torch
from sentence_transformers import SentenceTransformer, util
from datetime import datetime
import re  # For extracting year from job_end_year

def extract_year(date_str):
    """Extracts the year from a date string (e.g., 'Aug. 2020', '2005', 'current')."""
    if not date_str or date_str.lower() in {"current", "present", "now", "ongoing"}:
        return datetime.datetime.now().year  # Return current year

    match = re.search(r'(19\d{2}|20\d{2})', date_str)  # Look for a 4-digit year
    return int(match.group(0)) if match else None  # Convert to int if found

def score_and_rank_relevance(job_data=None, past_jobs=None, top_N=5, recency_weight=0.3, relevance_threshold=0.3, max_years_old=10):
    # Use GPU if available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

    # Unpack job_data
    (id, job_title, company_name, location, job_type, job_description,
     responsibilities, requirements, preferred_qualifications, technologies,
     soft_skills, salary_range, application_deadline, application_url,
     posting_date, job_id, hiring_manager, hiring_address) = job_data

    # Job posting text
    job_posting = f"""
    {job_title}\n{job_description}\n{requirements}\n{preferred_qualifications}\n{technologies}\n{soft_skills}
    """

    # Encode job posting once
    job_embedding = model.encode(job_posting, convert_to_tensor=True)

        # Process each past job independently
    filtered_jobs = {}
    # print(past_jobs.items())
    (company,
    location,
    title,
    start_date,
    end_date,
    field,
    responsibilities) = past_jobs
    print(f"{title} at {company}, {location} {start_date} - {end_date}.")
    responsibilities = responsibilities.split(";")

    # Extract year from the string
    job_end_year = extract_year(end_date)

    # Calculate years since job ended
    years_since_job = datetime.now().year - job_end_year

    # Encode all responsibilities for this job at once
    exp_embeddings = model.encode(responsibilities, convert_to_tensor=True)

    # Compute similarity scores
    similarities = util.pytorch_cos_sim(job_embedding, exp_embeddings).squeeze(0)

    # Calculate job-level metrics
    avg_relevance = similarities.mean().item()
    max_relevance = similarities.max().item()

    # Compute job recency score
    recency_score = max(0, 1 - (years_since_job / max_years_old))  # 1 if recent, 0 if too old
    weighted_score = (recency_weight * recency_score) + ((1 - recency_weight) * avg_relevance)
    print(f"RS = {recency_score:.3f}, WS = {weighted_score:.3f}")
    # Decision: Keep the job if it meets relevance and recency criteria
    if years_since_job > max_years_old and max_relevance < 0.3:
        print("Position is too old and irrelevant job duties.")
        return None

    if avg_relevance < relevance_threshold and max_relevance < 0.3:
        print("Position has no relevant job duties")
        return None

    # The positions that survive past this point are either recent enough or relevant enough to be included.
    # Select the top N most relevant responsibilities
    sorted_indices = torch.argsort(similarities, descending=True)[:top_N]
    top_responsibilities = [responsibilities[idx] for idx in sorted_indices if similarities[idx].item() > relevance_threshold - 0.1]
    # print(top_responsibilities)
    for idx in sorted_indices:
        print(f"Score: {similarities[idx].item():.3f} for {responsibilities[idx]}")

    return top_responsibilities


# # job_url = "https://www.governmentjobs.com/careers/tacoma/jobs/4779178/customer-service-representative"
# job_url = "https://jobs.jobvite.com/mariners/job/oU1uvfwE"
# # job_url = "https://www.usajobs.gov/job/832162900"
# db_path="resume.db"
# # job_data = get_job_postings(db_path=db_path, job_url=job_url)
# # print(len(job_data))
# job_data = get_scraped_job_data(db_path=db_path, job_url=job_url)
# employment = get_employment(db_path, 1)
# past_jobs = {}
# for position in employment:
#     # Corrected split usage
#     # past_jobs[f"{title} - {company}"] = [end_date, responsibilities]#.split(';')]
# # for job in past_jobs:
# #     print(f"{job}: {past_jobs[job]}")
#     print(score_and_rank_relevance(job_data=job_data, past_jobs=position))
