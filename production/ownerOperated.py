# There are many checks that happen before we send a request to the server but this helps speed up the system a lot.

# this is an array of all of the drivers that we do not want to include in updating the omnitracks

ownerOperated = ["CHESS", "DEVAN1", "DJOHNSO1" , "HGEDI", "IPARSONS", "ISHARP",
                  "JHAMILT1", "JMILL1" , "JRODRIG1", "PMAPA", "RCOCHRAN", "RHUMME1", "WGAEDK1", "justin"]

def isOwnerOperated(operatorName):
    if operatorName in ownerOperated:
        return True
    else:
        return False

