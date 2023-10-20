
import inspect

class Application:
    pass

class FileSystem:
    pass

class Server:
    pass

class VirtualMachine:
    pass

class Package:
    pass 

class LogicalGroup:
    pass

class Scenario:
    pass

class Class:
    def noop(self):
        #print(inspect.stack())
        str = "" 
        for s in inspect.stack():
            str =  s.function + " => " + str
        print(str)
                
class CompletableFuture(Class):
    def wait(self):
        self.noop()

class Blob(Package):

    class ShareStoreConcurrencyController(Class):
        def updateCoreVersionMetadata(self):
            self.noop()

        def recordState(self):
            self.noop()

    class SharedStoreTransferManager(Class):
        def pullFileAsync(self):
            return CompletableFuture()

    class SharedStoreManager(Class):  
        def __init__(self):
            self.sscc = Blob.ShareStoreConcurrencyController()
            self.cpf = Blob.CorePullFeeder()
            self.sstm = Blob.SharedStoreTransferManager()
            self.cpt = Blob.CorePullTracker()
        def load(self):
            self.cpf.run()                
        
        def getCorePullTracker(self):
            return self.cpt

        def getBlobStorageProvider(self):
            self.noop()

    class CorePullerThread(Class):    
        def __init__(self):
            self.ptq = Blob.PullTaskQueue() 

        def run(self):
            pt = self.ptq.removeFirst()
            pt.pullCoreFromBlob(Blob.SharedStoreManager())
    
    class CoresToPullQueue(Class):

        def removeFirst(self):
            return Blob.CorePullTask() 
        
        def addDeduplicated(self):
            self.noop()

    class PullTaskQueue(Class):
        def addCore(self,c):
            self.noop()
        def removeFirst(self):
            return Blob.CorePullTask()

    class CorePullTracker(Class):   
        def __init__(self):
            self.q = Blob.CoresToPullQueue()   
        def enqueuePullFromSharedStore(self):
            self.enqueueForPull()
        def enqueueForPull(self):
            self.q.addDeduplicated()
        def getCoreToPull(self):
            return self.q.removeFirst()

    class CorePullFeeder(Class):  
        def __init__(self):
            self.q = Blob.PullTaskQueue()   
            self.cpt = Blob.CorePullTracker()
        def run(self):
            t = Blob.CorePullerThread()
            t.run()
            self.feedTheMonster()
        def feedTheMonster(self):
            c = self.cpt.getCoreToPull()
            self.q.addCore(c)


    class CorePullTask(Class):

        def createCorePushPull(self):
            return Blob.CorePushPull()
        def pullCoreFromBlob(self, s):
            cpp = self.createCorePushPull()
            cpp.pullUpdateFromBlob(s)
            s.sscc.updateCoreVersionMetadata()
            s.sscc.recordState()

    class CorePushPull(Class):
        def pullUpdateFromBlob(self,s):            
            self.pullBlobFiles(s)
            self.moveFilesFromTempToIndexDir()
        
        def pullBlobFiles(self,s):            
            cf = s.sstm.pullFileAsync()
            cf.wait()
        
        def moveFilesFromTempToIndexDir(self):
            self.noop()

        def pushToBlobStore(self):
            self.noop()

    class CorePusher(Class):
        def pushCoreToSharedStore(self):
            self.pushToBlobStore()

        def pushToBlobStore(self):
            cpp = Blob.CorePushPull()
            cpp.pushToBlobStore()

    class CorePuller(Class):
        def __init__(self):
            self.corePP = Blob.CorePushPull()

        def pullCoreFromSharedStore(self, cc):
            ssm = cc.getSharedStoreManager()
            bsp = ssm.getBlobStorageProvider()
            bc = bsp.getClient()
            bc.pullCoreMetadata()
            ssm.createCorePullPush()
            ssm.sscm.updateCoreVersionMetadata()
            ssm.sscm.recordState()

class Startup(LogicalGroup):

    class SolrConfig(Class):        
        def getRequestParsers(self):
            self.noop()

    class SolrIndexWriter(Class):        
        def commit(self):
            self.commitInternal()

        def commitInternal(self):
            self.prepareCommitInternal()
            self.finishCommit()

        def prepareCommitInternal(self):
            self.WriteReaderPool()
    
    class SolrCoreState(Class):   
        
        def __init__(self):
            self.iw = Startup.SolrIndexWriter()
        
        def getIndexWriter(self):
            return self.iw
        
        def getCommitLock(self):
            self.noop()

    class CommitUpdateCommand(Class):
        def prepareCommit(self):
            self.noop()

    class DirectUpdateHandler2(Class):        
        
        def __init__(self):
            self.scs = Startup.SolrCoreState()

        def addDoc(self):
            self.noop()

        def commit(self):
            cuc = Startup.CommitUpdateCommand()
            cuc.prepareCommit()
            l = self.scs.getCommitLock()
            l.lock()
            iw = self.scs.getIndexWriter()
            iw.commit()
            l.unlock()

    class UpdateRequestProcessorChain(Class):        
        def createProcessor(self):
            return Update.UpdateRequestProcessor1()
        


    class SolrCore(Class):  
        
        def __init__(self):     
            self.conf = Startup.SolrConfig()  
            self.processorChain = Startup.UpdateRequestProcessorChain()
            self.handler = Startup.DirectUpdateHandler2()    
        
        def getSolrConfig(self):
            return self.conf
        def getUpdateProcessorChain(self):
            return self.processorChain
        
        def execute(self):
            self.noop()

    class SolrCores(Class):

        def __init__(self):
            self.solrCores = Startup.SolrCore()

        def putCore(self):
            self.noop()
        def getCoreDescriptor(self):
            self.noop()
        def getCoreFromAnyList(self):
            return Startup.SolrCore()
        def createFromDescriptor(self):
            return Startup.SolrCore()




    class ConfigSet(Class):        
        pass

    class CoreConfigService(Class):        
        def loadConfigSet(self):
            cs = Startup.ConfigSet()

    class CollectionRef(Class):       
        def getLeadersReplicas(self):
            self.noop()

    class ClusterState(Class):       
        
        def __init__(self):
            self.collectionRef = Startup.CollectionRef()

        def getCollecionOrNull(self):
            return self.collectionRef

        def getLiveNodes(self):
            self.noop()
        
    class ZKStateReader(Class):  

        def __init__(self):
            self.clusterState = Startup.ClusterState()

        def getClusterState(self):
            return self.clusterState

    class ZKController(Class):   

        def __init__(self):
            self.zkStateReader = Startup.ZKStateReader()

        def getZKStateReader(self):                             
            return self.zkStateReader


    class ZKContainer(Class):   

        def __init__(self):
            self.zkController = Startup.ZKController()

        def getZKController(self):                             
            return self.zkController

    class CoreContainer(Class):  
        
        def __init__(self):
            self.zkContainer = Startup.ZKContainer()
            self.solrCores = Startup.SolrCores()
        
        def load(self):
            ccs = Startup.CoreConfigService()
            self.s = Blob.SharedStoreManager()
            self.s.load()
            self.createFromDescriptor()
            ccs.loadConfigSet()
            self.registerCore()
            self.solrCores.putCore()

        def registerCore(self):
            self.noop()
        def createFromDescriptor(self):
            self.noop()

        def getRequestHandler(self, reqtype):
            if reqtype == "update":
                return Update.ContentStreamHandlerBase()
            elif  reqtype == "select":
                return Search.SearchHandler()
            else:
                return AnyRequest.RequestHandlerBase()

        def getZKController(self):
            return self.zkContainer.getZKController()

        def getCore(self):
            return self.solrCores.getCoreFromAnyList()

        def getSharedStoreManager(self):
            return self.s

    class SolrDispatchFilter(Class):   
        def Init(self):
            self.cc = Startup.CoreContainer()
            self.cc.load()

        def doFilter(self,reqtype):
            h = AnyRequest.HttpSolrCall(reqtype) 
            h.call(self.cc)

    class Jetty(Class):
        def __init__(self):
            self.sdf = Startup.SolrDispatchFilter()
        def doStart(self):
            self.sdf.Init()

        def doFilter(self, reqtype):
            self.sdf.doFilter(reqtype)


    class Main(Class): 

        def start(self):
            j = Startup.Jetty()
            j.doStart() #myhash
            j.doFilter("update")
            j.doFilter("request")

class AnyRequest(LogicalGroup):

    class SolrQueryRequest(Class):
        def setParams(self):
            self.noop()
        def getCore(self):
            return Startup.SolrCore()

    class RequestHandlerBase(Class):
        def handleRequest(self):
            self.noop()
        def enqueuePullFromSharedStore(self):
            self.noop()
        def handleRequestBody(self, r):
            self.noop() 

    class HttpSolrCall(Class):     
        def __init__(self, reqtype):
            self.reqtype = reqtype

        def call(self, cc:Startup.CoreContainer):
            self.init(cc)

        def init(self, cc:Startup.CoreContainer): 
            sqr = AnyRequest.SolrQueryRequest()
            rh = cc.getRequestHandler(self.reqtype)
            self.getCoreByCollection(cc)                
            c = self.randomlyGetSolrCore()
            conf = c.getSolrConfig()
            conf.getRequestParsers()
            self.addCommitIfAbsent(sqr)
            self.enqueuePullFromSharedStore(cc)
            self.execute(sqr, rh)

        def randomlyGetSolrCore(self):
            return Startup.SolrCore()

        def getCoreByCollection(self, cc:Startup.CoreContainer):  
            zkc = cc.getZKController()
            zkr = zkc.getZKStateReader()
            cs = zkr.getClusterState()
            col = cs.getCollecionOrNull()
            cs.getLiveNodes()
            col.getLeadersReplicas()
        
        def addCommitIfAbsent(self, sqr):  
            sqr.setParams() # commit=true
        
        def enqueuePullFromSharedStore(self,cc:Startup.CoreContainer):
            ssm = cc.getSharedStoreManager()
            cpt = ssm.getCorePullTracker()
            cpt.enqueueForPull()

        def execute(self, sqr, rh):  
            c = sqr.getCore()
            c.execute()
            rh.handleRequest()
            rh.enqueuePullFromSharedStore()
            rh.handleRequestBody(sqr) #( select/update)
        

class Search(LogicalGroup):
    class SolrComponent3(Class):        
        def prepare(self):
            self.noop()
        def process(self):
            self.noop()

    class SolrComponent2(Class):  
        
        def __init__(self):
            self.sc2 = Search.SolrComponent3()      
        def prepare(self):
            self.sc3.prepare()
        def process(self):
            self.sc3.process()    

    class SolrComponent1(Class):        
        def __init__(self):
            self.sc2 = Search.SolrComponent2()      
        def prepare(self):
            self.sc2.prepare()
        def process(self):
            self.sc2.process()  

    class SearchHandler(AnyRequest.RequestHandlerBase):        
        def handleRequestBody(self,r:AnyRequest.SolrQueryRequest):
            sc1 = self.getComponents()
            self.getAndPrepShardHAndler()
            sc1.prepare()
            sc1.process()

        def getComponents(self):
            self.noop()

class Update(LogicalGroup):
    class UpdateRequestProcessor3(Class):
        def processCommit(self):
            self.noop()
        def processAdd(self):
            self.noop()

    class UpdateRequestProcessor2(Class):
        def __init__(self):
            self.up3 = Update.UpdateRequestProcessor3()
        def processCommit(self):
            self.up3.processCommit()
        def processAdd(self):
            self.up3.processAdd()

    class UpdateRequestProcessor1(Class):
        def __init__(self):
            self.up2 = Update.UpdateRequestProcessor2()
        def processCommit(self):
            self.up2.processCommit()
        def processAdd(self):
            self.up2.processAdd()

    class ContentStreamHandlerBase(AnyRequest.RequestHandlerBase):       
        def handleRequestBody(self, r:AnyRequest.SolrQueryRequest):
            c = r.getCore()
            pc = c.getUpdateProcessorChain()
            up1 = pc.createProcessor()
            l = Update.JsonLoader()
            l.load()
            up1.processCommit()

    class JsonLoader(Class):        
        def load(self):
            t= Update.SingleThreadedJsonLoader()
            t.load()

    class SingleThreadedJsonLoader(Class):
        def __init__(self):
            self.up1 = Update.UpdateRequestProcessor1()
  
        def load(self):
            Update.SingleThreadedJsonLoader().processUpdate()
        def processUpdate(self):
            self.up1.processAdd()
            self.up1.processCommit()

    class SharedStoreIndexBatchProcessor(Class):
        def addOrDeleteGoingToBeIndexedLocally(self):
            self.startIndexingBatch()
            self.acquireWriteLockAndPull()
            cp = Blob.CorePuller()
            cp.pullCoreFromSharedStore()

        def hardCommitCompletedLocally(self):
            self.finishIndexingBatch()
            cp = Blob.CorePuller()
            cp.pushCoreToSharedStore()
        


class EBS(FileSystem):

    color = [35,107,142,1] #BLUE_E

    def BlobDataDir(self): 
        self.toto()
        self.titi()           


class Scenario:
    def Myscenario(self): 
        self.toto()
        self.titi()     

class SolrNode(Server):
    m = Startup.Main()

class S3(FileSystem):
    pass

class MyApp(Application):
    node = SolrNode()
    s3 = S3()
    def start(self):
        self.node.m.start()
    
if __name__ == "__main__":
   a = MyApp()
   a.start()