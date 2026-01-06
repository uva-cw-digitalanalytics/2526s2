import pandas as pd 
import os
import json
import sys
import datetime


def parse_instagram(username):
    posts = []
    comments = []
    with open(username+'/'+username+'.json', 'r') as f:
        data = json.loads(f.read())

    for item in data:
        for comment in item['comments']['data']:
            comment['created_at'] = datetime.datetime.fromtimestamp(comment['created_at'])
            comment['post_id'] = item['shortcode']
            comment['post_url'] = 'https://www.instagram.com/p/' + item['shortcode']
            comment['username'] = comment['owner']['username']
            comments.append(comment)

        del item['comments']
        item['post_url'] = 'https://www.instagram.com/p/' + item['shortcode']
        item['height'] = item['dimensions']['height']
        item['width'] = item['dimensions']['width']
        item['likes'] = item['edge_media_preview_like']['count']
        try:
            item['caption'] = item['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            pass
        item['comments'] = item['edge_media_to_comment']['count']
        item['created_at'] = datetime.datetime.fromtimestamp(item['taken_at_timestamp'])
        posts.append(item)

    posts = pd.DataFrame(posts)
    comments = pd.DataFrame(comments)
    posts.to_pickle(username+'_posts.pkl', index=False)
    comments.to_pickle(username+'_comments.pkl', index=False)




if __name__ == '__main__':
    if len(sys.argv) == 2:
        username = sys.argv[1]
        parse_instagram(username)
    else:
        print("You need to indicate a Instagram user while running the script. \n\n For example:\n python parse_instagram.py adidas")




