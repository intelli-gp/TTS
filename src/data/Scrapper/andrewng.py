import requests
from bs4 import BeautifulSoup
import csv

page=requests.get("https://www.coursera.org/instructor/andrewng")

def main(page):

    src=page.content
    soup=BeautifulSoup(src,"lxml")
    courses_details=[]
    courses_page_data = soup.find("div",{'class':'cds-9 css-1gh0hrn cds-10'}) #btl3 kol 7aga le kolo

    print(courses_page_data)
    # # i_tag=courses_page_data.i.extract()
    # for i in range (len(courses_title)):
    #     print(a_tag[i])
    def get_course_info(courses_page_data):
        for i in range(len(courses_page_data)):
        
            a_tag = courses_page_data.contents[i].a['href']
            courses_details.append({f"{i+1}-course link":f"https://www.coursera.org{a_tag}"})

        courses_title=courses_page_data.find_all('a',{'id':'instructors-course-card'})
        # print(courses_title)
            #  courses_details.append({"course name":a_tag})
        
    # for i in range(len(courses_page_data)):
        
    get_course_info(courses_page_data)
    for i in range (len(courses_details)):
        print(courses_details[i])
    #         print(a_tag[i])
    # keys = courses_details[0].keys()
    # with open ('.csv','w',encoding="utf-8") as output_file:
    #     dict_writer = csv.DictWriter(output_file, keys)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(courses_details)
    #     print("file created")

main(page)