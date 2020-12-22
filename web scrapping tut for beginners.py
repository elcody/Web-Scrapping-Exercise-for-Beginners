# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 21:58:38 2020

@author: codyb
"""

import requests
from bs4 import BeautifulSoup

def extract_text(soup_obj, tag, attribute_name, attribute_value):
    response = soup_obj.find(tag, {attribute_name: attribute_value}).text.strip() if soup_obj.find(tag, {attribute_name: attribute_value}) else ''
    return response

def main(url):
    try:
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        course_title = extract_text(soup, 'h1', 'data-purpose', 'lead-title')

        if course_title:
            headline = extract_text(soup, 'div', 'data-purpose', 'lead-headline')
            rating = extract_text(soup, 'span', 'data-purpose', 'rating-number')
            last_updated = extract_text(soup, 'div', 'data-purpose', 'last-update-date')

            course_objectives = soup.find('ul', {'class': 'unstyled-list udlite-block-list what-you-will-learn--objectives-list--2cWZN'})
            object_items = course_objectives.find_all('li')

            summary_bullets = {}
            for indx, val in enumerate(object_items):
                summary_bullets[indx] = val.text

            course_description = extract_text(soup, 'div', 'data-purpose', 'safely-set-inner-html:description:description')

            course_content = soup.find('div', {'data-purpose': 'course-curriculum'})
            lesson_names = course_content.find_all('li')

            lessons = []
            for lesson_name in lesson_names:
                lessons.append('- ' + lesson_name.span.text.strip())

            print('Course Title: {0}'.format(course_title))
            print('Headline: {0}'.format(headline))
            print('Rating: {0}'.format(rating))
            print(last_updated)
            print('Course Description:')
            print(course_description)
            print('')
            print('Course Objectives')
            print('*' * 50)
            print(*summary_bullets.items(), sep='\n')
            print('')
            print('Lessons:')
            print('-' * 50)
            print(*lessons, sep='\n')
    except Exception as e:
        print('Information not available')

url = input('Enter course URL: ')
if url:
    main(url)