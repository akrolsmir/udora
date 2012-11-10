import youtube
import youtube.service
yt_service = youtube.service.YouTubeService()
yt_service.developer_key = "AI39si660GlKcr0GUhyUAkwD1cgwTp3-tvJwLHxzieVrv7SDmDIXIPXjTsopJBT-It3WySFI3G8K42ICC3G2341NOZC9HL8i2A"
class Udora(object):
    def __init__(self,url):
        self.nextInQueue={url:1010}
        self.previouslyPlayed=[]
        self.x = 1000
        
    def getRelatedVidID(self,feed):
        for entry in feed.entry:
            url=entry.media.player.url[32:43]
            if url in self.previouslyPlayed:
                break
            elif url not in self.nextInQueue:
                self.nextInQueue[url]=self.x
                self.x= self.x-1
            else:
                self.nextInQueue[url]=self.nextInQueue[url]+10
                
    def updateDict(self):
        length=len(self.nextInQueue)
        for i in self.nextInQueue.keys():
            self.getRelatedVidID(yt_service.GetYouTubeRelatedVideoFeed(video_id=i))
            
    def getHighestURL(self):
        highestNum=0
        highestID=""
        if len(self.nextInQueue)==0:
            return ""
        for i in self.nextInQueue.keys():
            if self.nextInQueue[i]>highestNum:
                highestNum = self.nextInQueue[i]
                highestID=i
        self.previouslyPlayed.append(highestID)
        self.nextInQueue.pop(highestID)
        self.getRelatedVidID(yt_service.GetYouTubeRelatedVideoFeed(video_id=highestID))
        return highestID

    def subtractRanking(self,feed):
        for entry in feed.entry:
            url=entry.media.player.url[32:43]
            if url in self.previouslyPlayed:
                break
            elif url not in self.nextInQueue:
                self.nextInQueue[url]=0
            else:
                self.nextInQueue[url]=self.nextInQueue[url]-1
                
    def changeRanking(self,isUp,url):
        feed=yt_service.GetYouTubeRelatedVideoFeed(video_id=url)
        if isUp:
            self.getRelatedVidID(feed)
        else:
            self.subtractRanking(feed)
            
