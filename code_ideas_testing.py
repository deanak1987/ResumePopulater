# from sentence_transformers import SentenceTransformer, util
# from job_posting_scraper_ai import get_scraped_job_data
# from db_manager import get_employment, get_job_postings
# import torch
#
# def score_and_rank_relevance(job_disc_data=None, past_employment=None):
#     # Use GPU if available
#     device = 'cuda' if torch.cuda.is_available() else 'cpu'
#     model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
#
#     (job_title, company_name, loc, job_type, job_description,
#      duties, requirements, preferred_qualifications, technologies,
#      soft_skills, salary_range, application_deadline, application_url,
#      posting_date, job_id, hiring_manager, hiring_address) = job_disc_data
#
#     # Job posting text
#     job_posting = f"""
#     {job_title}\n{job_description}\n{requirements}\n{preferred_qualifications}\n{technologies}\n{soft_skills}
#     """
#
#     # Encode job posting once
#     print(f"Encoding data for job posting:\n{company_name} in {loc}, {job_type} with salary: {salary_range}")
#     print(f"Job ID: {job_id} Posted {posting_date}, Application deadline: {application_deadline}\nPosting URL: {application_url}")
#     job_embedding = model.encode(job_posting, convert_to_tensor=True)
#
#     # Process each past job independently
#     # top_N = 11  # Adjust to keep the top N most relevant responsibilities per job
#     output = []
#     for job_title, duties in past_employment.items():
#         print(f"\nJob: {job_title}")
#         top_N = len(duties)
#         # Encode all responsibilities for this job at once
#         exp_embeddings = model.encode(duties, convert_to_tensor=True)
#
#         # Compute similarity scores
#         similarities = util.pytorch_cos_sim(job_embedding, exp_embeddings).squeeze(0)
#
#         # Sort by highest relevance
#         sorted_indices = torch.argsort(similarities, descending=True)[:top_N]
#         resp = []
#         # Display top matches for this specific job
#         for rank, idx in enumerate(sorted_indices, start=1):
#             print(f"  Rank {rank} | Score: {similarities[idx].item():.3f}")
#             print(f"  Responsibility: {duties[idx]}\n")
#             resp.append(duties[idx])
#         output.append(resp)
#     return output
#
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
#     (
#         company,
#         location,
#         title,
#         start_date,
#         end_date,
#         field,
#         responsibilities,
#     ) = position
#
#     # Corrected split usage
#     past_jobs[f"{title} - {company}"] = responsibilities.split(';')
# # for job in past_jobs:
# #     print(f"{job}: {past_jobs[job]}")
# print(score_and_rank_relevance(job_disc_data=job_data, past_employment=past_jobs))
