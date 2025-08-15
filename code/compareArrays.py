

#returns element that is absent in arr2
def compareArrs(a1, a2):
    for i in range(len(a2)):
        if(a1[i] != a2[i]):
            return a1[i]
    return a1[len(a1)-1]

# print(compareArrs(arr1, arr2))



# print(profile.followees) #number of following
# print(profile.followers) #number of followers
# print(profile.full_name) #full name
# print(profile.biography) #bio
# print(profile.profile_pic_url)  #profile picture url 
# print(profile.get_posts()) #list of posts
# print(profile.get_followees()) #list of followees









