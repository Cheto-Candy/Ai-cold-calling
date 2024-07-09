import requests
from datetime import datetime
from groq import Groq
import time

system_prompt = 'TechRealm sells seo,digital marketing,web development and more' 
system_company = 'techrealm'

def execute(promt):
    client = Groq(api_key="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")
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": promt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )
    response=''
    for chunk in completion:
        response+=chunk.choices[0].delta.content or ""
    return response


def ectrct_lead(lead):
    promt=f"""
Extract the name and number from the following lead and return it in the form of a Python dictionary:
Lead: {lead}

Only provide the dictionary as the output key of dectionary (name,phone with country code include) must in lowercasef. Do not include any additional text or explanation.
"""
    data=execute(promt)
    return eval(data)




def create_a_purpose(lead):
    promt=f'{lead} this is the details of a customer,our campny name is {system_company} {system_prompt}. you need to create a prompt for a marketing agent to tell him how to talk to the client what to present and most importantly what to ask the client about.'
    purpose=execute(promt)
    return purpose


def get_call_summary_from_vapi(call_Id):
    # Your Vapi API Authorization token
    auth_token = '16ca8436-91b6-49e7-b382-60d964aaf646'
    # The ID of the call you want to retrieve
    call_id = str(call_Id)

    # Create the header with Authorization token
    headers = {
        'Authorization': f'Bearer {auth_token}',
    }

    # Make the GET request to Vapi to retrieve the call details
    response = requests.get(
        f'https://api.vapi.ai/call/{call_id}',
        headers=headers
    )

    # Check if the request was successful and print the summary
    if response.status_code == 200:
        call_data = response.json()
        summary = call_data.get('analysis', {}).get('summary')
        if summary:
            return (summary)
        else:
            return None
    else:
        return None    
    
   
def fetch_call_analytics_from_vapi(call_id):

    api_key="16ca8436-91b6-49e7-b382-60d964aaf646"

    url = f"https://api.vapi.ai/call/{call_id}"  #
    headers = {
        "Authorization": f"Bearer {api_key}"  #
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        
        call_data = response.json()
        
        # Parse startedAt and endedAt to datetime objects
        started_at = datetime.fromisoformat(call_data.get("startedAt").replace("Z", "+00:00")) if call_data.get("startedAt") else None
        ended_at = datetime.fromisoformat(call_data.get("endedAt").replace("Z", "+00:00")) if call_data.get("endedAt") else None
        
        # Calculate duration
        duration = (ended_at - started_at).total_seconds() if ended_at and started_at else None
        
        # Extract relevant analytics data
        analytics = {
            "cost": call_data.get("cost"),
            # "cost_breakdown": call_data.get("costBreakdown"),
            "duration": duration,
            "status": call_data.get("status"),
            # "ended_reason": call_data.get("endedReason"),
            # "analysis": call_data.get("analysis"),
            # "transcript": call_data.get("transcript"),
            # "recording_url": call_data.get("recordingUrl")
        }
        
        return analytics
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching call analytics: {e}")
        return None

       


def check_lead(summary):
    promt=f'You are an AI bot made to analyze summaries, your output is limited to an answer of 1 or 0, 1 stands for if the lead is converted and 0 stands for if the lead is not converted. analyze the summary and answer in 1 or 0 {summary} using the summary analyze if the lead is converted or no if converted only reply with 1 if it is not then reply with'
    purpose=execute(promt)
    return purpose

# create a call

def create_a_call(purpose,customer_name,customer_number):
    # Your Vapi API Authorization token
    auth_token = '16ca8436-91b6-49e7-b382-60d964aaf646'
    # The Phone Number ID, and the Customer details for the call
    phone_number_id = '59269006-cf59-4a7e-b3d3-c94cf69ee940' 
    
    # Create the header with Authorization token
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json',
    }

    # Create the data payload for the API request

    data = {
        'assistant': {
            "firstMessage": f"Hey, is this {customer_name}?",
            "model": {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": f"You are an AI bot called jennifer,keep the conversation short try to address fast the aim is to get the user to sign up to calenderly for a meeting  you are made to tell a customer about the solutions {system_company} offers, you can use the informaton below to address the customer our servces are {system_prompt} and as follows keep the conversation short try to address fast the aim is to get the user to sign up to calenderly for a meeting {purpose}"
                    }
                ]
            },
            "voice": "jennifer-playht"
        },
        'phoneNumberId': phone_number_id,
        'customer': {
            'number': customer_number,
        },
    }

    # Make the POST request to Vapi to create the phone call
    response = requests.post(
        'https://api.vapi.ai/call/phone', headers=headers, json=data)


    # Check if the request was successful and print the response
    if response.status_code == 201:
        print('Call created successfully')
        response_data = response.json()
        # print(response_data)  # Get the dictionary from the response
    
    # Check if 'id' key exists (assuming id is the value you want)
        if 'id' in response_data:
            call_id = response_data['id']
            print(call_id)
            return call_id  # Print id with a label for clarity
        else:
            print("No 'id' key found in the response data.")
    else:
        print('Failed to create call')
        print(response.text)



def wait_for_call_completion(call_id, max_wait_time=300, check_interval=5):
    api_key='16ca8436-91b6-49e7-b382-60d964aaf646'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    url = f'https://api.vapi.ai/call/{call_id}'
    
    start_time = time.time()
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            call_data = response.json()
            if call_data['status'] == 'ended':
                print("Call has ended.")
                return call_data
        else:
            print(f"Error fetching call status: {response.status_code}")
        
        if time.time() - start_time > max_wait_time:
            print("Maximum wait time exceeded.")
            return None
        
        time.sleep(check_interval)







# from django.http import JsonResponse, HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from .models import Lead
# from django.db.models import Q
# import json
# import requests
# from firecrawl import FirecrawlApp
# import time
# import os
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from groq import Groq
# # from dotenv import load_dotenv
# # load_dotenv()


# google_api_key = 'AIzaSyDABn6AcIrsQO_7mzjy7KBervAU95xeY68'
# search_engine_id = "266ea662b6cf948b1"
# firecrawl_api_key = "fc-d2298444a58043ae8696fb35619e7e6f"
# # builtwith_api_key = os.getenv('BUILTWITH_API_KEY')
# # backlink_api_key = os.getenv('BACKLINK_API_KEY')
# # similarweb_api_key = os.getenv('SIMILARWEB_API_KEY')
# groq_api_key  = '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'



# @csrf_exempt
# def add_lead(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         contact_information = request.POST.get('contact_info')
#         industry = request.POST.get('industry')
#         location = request.POST.get('location')

#         if name and contact_information and industry and location:
#             lead = Lead.objects.create(
#                 name=name,
#                 contact_information=contact_information,
#                 industry=industry,
#                 location=location
#             )
#             return JsonResponse({'id': lead.id, 'status': 'Lead added'}, status=201)
#         return JsonResponse({'error': 'Invalid input'}, status=400)
#     return HttpResponse(status=405)

# @csrf_exempt
# def get_or_update_lead(request, id):
#     try:
#         lead = Lead.objects.get(id=id)
        
#         if request.method == 'PUT':
#             data = json.loads(request.body)
#             name = data.get('name')
#             contact_info = data.get('contact_info')
#             industry = data.get('industry')
#             location = data.get('location')
#             notes = data.get('notes')
#             if name:
#                 lead.name = name
#             if contact_info:
#                 lead.contact_information = contact_info
#             if industry:
#                 lead.industry = industry
#             if location:
#                 lead.location = location
#             if notes:
#                 lead.notes = notes

#             lead.save()
#             return JsonResponse({'id': lead.id, 'name': lead.name, 'industry': lead.industry, 'status': 'Lead updated'})

#         elif request.method == 'GET':
#             # Handle GET request to retrieve lead details
#             lead_data = {
#                 'id': lead.id,
#                 'name': lead.name,
#                 'contact_info': lead.contact_information,
#                 'industry': lead.industry,
#                 'location': lead.location,
#                 'notes': lead.notes
#             }
#             return JsonResponse(lead_data)

#         else:
#             return HttpResponse(status=405)  # Method Not Allowed for other methods
    
#     except Lead.DoesNotExist:
#         return JsonResponse({'error': 'Lead not found'}, status=404)

# @csrf_exempt
# def find_leads(request):
#     query = request.GET.get('query', '')
    
#     leads = Lead.objects.filter(
#         Q(industry__icontains=query) |
#         Q(location__icontains=query) |
#         Q(name__icontains=query) |
#         Q(contact_information__icontains=query)
#     )

#     leads_data = [{
#         'id': lead.id,
#         'name': lead.name,
#         'contact_info': lead.contact_information,
#         'industry': lead.industry,
#         'location': lead.location,
#         'notes': lead.notes
#     } for lead in leads]
    
#     return JsonResponse(leads_data, safe=False)


# @csrf_exempt
# def add_notes(request, id):
#     try:
#         lead = Lead.objects.get(id=id)
#         if request.method == 'POST':
#             notes = request.POST.get('notes')
#             if notes:
#                 lead.notes = lead.notes + '\n' + notes if lead.notes else notes
#                 lead.save()
#                 return JsonResponse({'id': lead.id, 'status': 'Notes added'})
#             return JsonResponse({'error': 'No notes provided'}, status=400)
#         return HttpResponse(status=405)
#     except Lead.DoesNotExist:
#         return JsonResponse({'error': 'Lead not found'}, status=404)


# client = Groq(api_key=groq_api_key)

# def summarize_text(text):
#     try:
#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {
#                     "role": "user",
#                     "content": f"Summarize the following text and generate a comprehensive summary about the brand, including key details and unique selling points: {text}",
#                 }
#             ],
#             model="llama3-8b-8192",
#         )
#         return chat_completion.choices[0].message.content.strip()
#     except Exception as e:
#         return f"Error in summarization: {str(e)}"

# @csrf_exempt
# def find_shopify_stores(request):
#     if request.method == 'GET':
#         industry = request.GET.get('industry', '')
#         location = request.GET.get('location', '')

#         if not (industry and location):
#             return JsonResponse({'error': 'Industry and location parameters are required'}, status=400)

#         query = f'inurl:myshopify.com {industry} {location}'
#         url = f"https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={search_engine_id}&q={query}"

#         try:
#             response = requests.get(url)
#             response.raise_for_status()  # Raise an error for bad status codes
#             results = response.json()
#         except requests.RequestException as e:
#             return JsonResponse({'error': f"Google Custom Search API error: {str(e)}"}, status=500)
#         except ValueError:
#             return JsonResponse({'error': 'Invalid JSON in Google Custom Search API response'}, status=500)

#         final_links = []
#         email_contents = []

#         if not firecrawl_api_key:
#             return JsonResponse({'error': 'Firecrawl API key is not set'}, status=500)

#         app = FirecrawlApp(api_key=firecrawl_api_key)

#         for item in results.get('items', []):
#             final_links.append(item['link'])

#             # Retry mechanism for rate limiting
#             retry_count = 0
#             while retry_count < 5:
#                 try:
#                     scraped_data = app.scrape_url(item['link'])
#                     if scraped_data and 'content' in scraped_data and scraped_data['content']:
#                         content = scraped_data['content']
#                         print("Markdown content:", content)

#                         # Split text into manageable chunks for summarization
#                         max_chunk_size = 500  # Adjust as needed
#                         chunks = [content[i:i + max_chunk_size] for i in range(0, len(content), max_chunk_size)]

#                         # Summarize each chunk and concatenate results
#                         brand_summary = ""
#                         for chunk in chunks:
#                             chunk_summary = summarize_text(chunk)
#                             brand_summary += chunk_summary + " "

#                         # Use BuiltWith to get technology stacks
#                         builtwith_url = f"https://api.builtwith.com/free1/api.[xml|json]?KEY={builtwith_api_key}&LOOKUP={item['link']}"
#                         try:
#                             bw_response = requests.get(builtwith_url)
#                             bw_response.raise_for_status()
#                             bw_data = bw_response.json()
#                         except requests.RequestException as e:
#                             bw_data = {'Errors': str(e)}
#                         except ValueError:
#                             bw_data = {'Errors': 'Invalid JSON in BuiltWith API response'}
#                         print("BuiltWith data:", bw_data)

#                         if bw_data.get('Errors'):
#                             # Log error if there are any
#                             print(f"BuiltWith API Error for {item['link']}: {bw_data['Errors']}")

#                         technology_stacks = bw_data.get('Groups', [])

#                         # Add backlink checking functionality
#                         backlink_api_url = f"https://api.seoreviewtools.com/backlinks/?url={item['link']}&key={backlink_api_key}"
#                         try:
#                             backlink_response = requests.get(backlink_api_url)
#                             backlink_response.raise_for_status()
#                             backlink_data = backlink_response.json()
#                             backlink_count = backlink_data.get('backlinks', 0)
#                         except requests.RequestException as e:
#                             backlink_count = 0
#                         except ValueError:
#                             backlink_count = 0

#                         # Add traffic analysis functionality
#                         traffic_api_url = f"https://api.similarweb.com/v1/website/{item['link']}/traffic-and-engagement/visits?api_key={similarweb_api_key}"
#                         try:
#                             traffic_response = requests.get(traffic_api_url)
#                             traffic_response.raise_for_status()
#                             traffic_data = traffic_response.json()
#                             traffic_visits = traffic_data.get('visits', 0)
#                         except requests.RequestException as e:
#                             traffic_visits = 0
#                         except ValueError:
#                             traffic_visits = 0

#                         # Generate HTML email template
#                         email_subject = f"Exploring Collaboration Opportunities with {item['link']}"
#                         email_body_html = render_to_string('email_template.html', {
#                             'item_link': item['link'],
#                             'brand_summary': brand_summary.strip(),
#                             'technology_stacks': technology_stacks,
#                             'backlink_count': backlink_count,
#                             'traffic_visits': traffic_visits,
#                         })
#                         email_body_text = strip_tags(email_body_html)  # Strip HTML tags for text version
#                         print("email_body_text:", email_body_text)

        
#                         email_contents.append({
#                             "link": item['link'],
#                             "summary": brand_summary.strip(),
#                             "technology stacks": technology_stacks,
#                             "backlink_count": backlink_count,
#                             "traffic_visits": traffic_visits,
#                             "email_subject": email_subject,
#                             "email_body_html": email_body_html
#                         })
#                     else:
#                         email_contents.append({
#                             "link": item['link'],
#                             "summary": "No content available",
#                             "email_subject": email_subject,
#                             "email_body_html": "No content available"
#                         })

#                     break
#                 except requests.RequestException as e:
#                     if 'rate limit exceeded' in str(e).lower():
#                         retry_count += 1
#                         wait_time = 2 ** retry_count
#                         time.sleep(wait_time)
#                     else:
#                         # Log the exception for debugging
#                         print(f"Error processing {item['link']}: {str(e)}")
#                         email_contents.append({
#                             "link": item['link'],
#                             "summary": f"Error: {str(e)}",
#                             "email_subject": email_subject,
#                             "email_body_html": f"Error: {str(e)}"
#                         })
#                         break
#                 except Exception as e:
#                     # Log any other unexpected exceptions
#                     print(f"Unexpected error processing {item['link']}: {str(e)}")
#                     email_contents.append({
#                         "link": item['link'],
#                         "summary": f"Error: {str(e)}",
#                         "email_subject": email_subject,
#                         "email_body_html": f"Error: {str(e)}"
#                     })
#                     break

#         return JsonResponse({"Links": final_links, "EmailContents": email_contents})
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
