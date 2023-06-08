##
##
##class ContinueI(Exception):
##    pass
##
##
##continue_i = ContinueI()
##
##for i in [1,2,3,4,5,6]:
##    try:
##        for j in ["a","b","c","d","e","f"]:
##            if j == "d":
##                raise continue_i
##            print(f"{i}:{j}")
##    except ContinueI:
##        continue


class Continue_First(Exception):
        pass


def filter_videos():
    continue_video = Continue_First()

    videos = []
    for video in [1,2,3,4,5,6]:
        try:
            for param in ["a","b","c","d","e","f"]:
                if param == "d":
                    raise continue_video
                videos.append(video)
        except Continue_First:
            continue
    return videos

print(filter_videos())
    
