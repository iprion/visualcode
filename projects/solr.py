AppName = "ROOT"
color = [187,187,187,1] #LIGHT_GRAY

class Node1:

    color = [221,221,221,1] #LIGHTER_GRAY

    class Startup:

        color = [88,196,221,0.1] #BLUE      

        class Main: 

            def start(self):
                Startup.Jetty()
                Startup.Jetty.doStart() #myhash

        class Jetty:
            def doStart(self):
                Startup.SolrDispatchFilter.Init()

            def doFilter(self):
                Startup.SolrDispatchFilter.doFilter()

        class SolrDispatchFilter:   
            def Init(self):
                Startup.CoreContainer()
                Startup.CoreContainer.load()

            def doFilter(self):
                Node1.AnyRequest.HttpSolrCall()
                Node1.AnyRequest.HttpSolrCall.call()


        class CoreContainer:  
            
            zkContainer = Startup.ZKContainer()
            solrCores = Startup.SolrCores()
            
            def load(self):
                Startup.CoreConfigService()
                Node1.Blob.SharedStoreManager()
                Node1.Blob.SharedStoreManager.load()
                createFromDescriptor()
                Startup.CoreConfigService.loadConfigSet()
                registerCore()
                Startup.SolrCores.putCore()

            def getRequestHandler(self):
                pass

            def getZKController(self):
                pass

            def getCore(self):
                Startup.SolrCores.getCoreFromAnyList()

            def getSharedStoreManager(self):
                pass


        class ZKContainer:   

            zkController = Startup.ZKController()
     
            def getZKController(self):                             
                pass

        class ZKController:   

            zkStateReader = Startup.ZKStateReader()

            def getZKStateReader(self):                             
                pass

        class ZKStateReader:  

            clusterState = Startup.ClusterState()
      
            def getClusterState(self):
                pass

        class ClusterState:       
            
            collectionRef = Startup.CollectionRef()

            def getCollecionOrNull(self):
                pass

            def getLiveNodes(self):
                pass

        class CollectionRef:       
            pass

        class SolrConfig:        
            def getRequestParsers(self):
                pass

        class CoreConfigService:        
            def loadConfigSet(self):
                Startup.ConfigSet()

        class ConfigSet:        
            pass

        class SolrCores:       
            
            solrCores = Startup.SolrCore()

            def putCore(self):
                pass
            def getCoreDescriptor(self):
                pass
            def getCoreFromAnyList(self):
                pass

        class SolrCore:  
            conf = Startup.SolrConfig()  
            processorChain = Startup.UpdateRequestProcessorChain()
            handler = Startup.DirectUpdateHandler2()    
            
            def getSolrConfig(self):
                pass
            def getUpdateProcessorChain(self):
                pass

        class UpdateRequestProcessorChain:        
            def createProcessor(self):
                pass

        class SolrCoreState:        
            def getIndexWriter(self):
                pass
            def getCommitLock(self):
                pass
        
        class DirectUpdateHandler2:        
            def addDoc(self):
                pass
            def commit(self):
                Startup.CommitUpdateCommand.prepareCommit()
                Startup.SolrCoreState.getCommitLock()
                Startup.CommitLock.lock()
                Startup.SolrCoreState.getIndexWriter()
                Startup.SolrIndexWriter.commit()
                SolrCoreState.getCommitLock()
                SolrCoreState.CommitLock.unlock()

        class SolrIndexWriter:        
            def commit(self):
                SolrIndexWriter.commitInternal()

            def commitInternal(self):
                SolrIndexWriter.prepareCommitInternal()
                finishCommit()

            def prepareCommitInternal(self):
                SolrIndexWriter.WriteReaderPool()

    class AnyRequest:

        color = [131,193,103,0.1] #GREEN
        
        class HttpSolrCall:        
            def call(self):
                HttpSolrCall.init()

            def init(self): 
                Node1.Startup.CoreContainer.getRequestHandler()
                HttpSolrCall.getCoreByCollection()                
                HttpSolrCall.randomlyGetSolrCore()
                Node1.Startup.SolrCore.getSolrConfig()
                Node1.Startup.SolrConfig.getRequestParsers()
                HttpSolrCall.addCommitIfAbsent()
                HttpSolrCall.enqueuePullFromSharedStore()
                HttpSolrCall.execute()

             
            def getCoreByCollection(self):  
                Node1.Startup.CoreContainer.getZKController()
                Node1.Startup.ZKController.getZKStateReader()
                Node1.Startup.ZKStateReader.getClusterState()
                Node1.Startup.ClusterState.getCollecionOrNull()
                Node1.Startup.ClusterState.getLiveNodes()
                Node1.Startup.DocCollection.getLeadersReplicas()
            
            def addCommitIfAbsent(self):  
                SolrQueryRequest.setParams() # commit=true
            
            def enqueuePullFromSharedStore(self):
                Node1.Startup.CoreContainer.getSharedStoreManager()
                Node1.Blob.SharedStoreManager.getCorePullTracker()
                Node1.Blob.CorePullTracker.enqueueForPull()

            def execute(self):  
                SolrQueryRequest.getCore()
                SolrCore.execute()
                RequestHandlerBase.handleRequest()
                RequestHandlerBase.enqueuePullFromSharedStore()
                Node1.Select.SearchHandler.handleRequestBody()
                Node1.Update.ContentStreamHandlerBase.handleRequestBody()

    class Select:
    
        color = [202,163,232,0.1] # PURPLE_A
        
        class SearchHandler:        
            def handleRequestBody(self):
                getComponents()
                getAndPrepShardHAndler()
                Select.SolrComponent1.prepare()
                Select.SolrComponent1.process()

        class SolrComponent1:        
            def prepare(self):
                Select.SolrComponent2.prepare()
            def process(self):
                Select.SolrComponent2.process()

        class SolrComponent2:        
            def prepare(self):
                Select.SolrComponent3.prepare()
            def process(self):
                Select.SolrComponent3.process()              
       
        class SolrComponent3:        
            def prepare(self):
                pass
            def process(self):
                pass

    class Update:
    
        color = [255,255,0,0.1] #YELLOW
    
        class ContentStreamHandlerBase:       
            def handleRequestBody(self):
                SolrQueryRequest.getCore()
                Startup.SolrCore.getUpdateProcessorChain()
                Node1.Startup.UpdateRequestProcessorChain.createProcessor()
                Update.JsonLoader()
                Update.JsonLoader.load()
                Update.UpdateRequestProcessor1.processCommit()
        
        class UpdateRequestProcessor1:
            def processCommit(self):
                Update.UpdateRequestProcessor2.processCommit()
            def processAdd(self):
                Update.UpdateRequestProcessor2.processAdd()

        class UpdateRequestProcessor2:
            def processCommit(self):
                Update.UpdateRequestProcessor3.processCommit()
            def processAdd(self):
                Update.UpdateRequestProcessor3.processAdd()

        class UpdateRequestProcessor3:
            def processCommit(self):
                pass
            def processAdd(self):
                pass

        class JsonLoader:        
            def load(self):
                Update.SingleThreadedJsonLoader.load()

        class SingleThreadedJsonLoader:
            def load(self):
                SingleThreadedJsonLoader.processUpdate()
            def processUpdate(self):
                Update.UpdateRequestProcessor1.processAdd()
                Update.UpdateRequestProcessor1.processCommit()
        
        class SharedStoreIndexBatchProcessor:
            def addOrDeleteGoingToBeIndexedLocally(self):
                startIndexingBatch()
                acquireWriteLockAndPull()
                Blob.CorePuller.pullCoreFromSharedStore()

            def hardCommitCompletedLocally(self):
                finishIndexingBatch()
                Node1.Blob.CorePusher.pushCoresToSharedStore()


    class Blob:      
    
        color = [35,107,142,0.1] #BLUE_E
        
        class SharedStoreManager:      
            def load(self):
                Blob.CorePullFeeder.run()                
            
            def getCorePullTracker(self):
                pass

            def getBlobStorageProvider(self):
                pass

        class CorePullerThread:     
            def run(self):
                Blob.PullTaskQueue.removeFirst()
                Blob.CorePullTask.pullCoreFromBlob()

        class CorePullTracker:      
            def enqueuePullFromSharedStore(self):
                CorePullTracker.enqueueForPull()
            def enqueueForPull(self):
                Blob.CoresToPullQueue.addDeduplicated()
            def getCoreToPull(self):
                Blob.CoresToPullQueue.removeFirst()
        
        class CoresToPullQueue:
            def removeFirst(self):
                pass
            def addDeduplicated(self):
                pass

        class CorePullFeeder:      
            def run(self):
                Blob.CorePullerThread()
                Blob.CorePullerThread.run()
                CorePullFeeder.feedTheMonster()
            def feedTheMonster(self):
                Blob.CorePullTracker.getCoreToPull()
                Blob.PullTaskQueue.addCore()
        
        class PullTaskQueue:
            def addCore(self):
                pass
            def removeFirst(self):
                pass

        class CorePullTask:
            def pullCoreFromBlob(self):
                Blob.SharedStoreManager.createCorePushPull()
                Blob.CorePushPull.pullUpdateFromBlob()
                Blob.SharedStoreConcurrencyManager.updateCoreVersionMetadata()
                Blob.SharedStoreConcurrencyManager.recordState()

        class CorePushPull:
            def pullUpdateFromBlob(self):            
                CorePushPull.pullBlobFiles()
                moveFilesFromTempToIndexDir()
            
            def pullBlobFiles(self):            
                Blob.ShareTransferManager.pullFileAsync()
                CompletableFuture.wait()
            
            def pushToBlobStore(self):
                pass

        class CorePusher:
            def pushCoreToSharedStore(self):
                Blob.CorePusher.pushToBlobStore()

            def pushToBlobStore(self):
                Blob.CorePushPull.pushToBlobStore()

        class CorePuller:
            
            corePP = Blob.CorePushPull()

            def pullCoreFromSharedStore(self):
                Startup.CoreContainer.getSharedStoreManager()
                Blob.SharedStoreManager.getBlobStorageProvider()
                Blob.BlobStorageProvider.getClient()
                Blob.BlobClient.pullCoreMetadata()
                Blob.SharedStoreManager.createCorePullPush()
                Blob.ShareStoreConcurrencyController.updateCoreVersionMetadata()
                Blob.ShareStoreConcurrencyController.recordState()


    class EBS:
    
        color = [35,107,142,1] #BLUE_E

        def BlobDataDir(self): 
            toto()
            titi()           

class Node2:       

    color = [221,221,221,1] #LIGHTER_GRAY
    
    class class1:              
    
        color = [35,107,142,0.1] #BLUE_E

        def func1(self):
            toto()
            titi()
            tutu()
            solr.Node1.func()
            this.Function()
            this.toto()
    
    class class2:              
        
        color = [35,107,142,0.1] #BLUE_E
        
        def func1(self):
            toto()
            titi()
            tutu()
            solr.Node1.func()
            this.Function()
            toto()

class MyScenario:
    def Launch(self): 
        ROOT.Node1.Startup.Main.start()