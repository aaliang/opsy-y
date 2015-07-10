var AWS = require('aws-sdk'),
    moment = require('moment');
    
//automation script to remove(deregister) stale aws amis

var sortByCreationTime = function (a, b) {
  if (a._creationTime > b._creationTime) return 1;
  if (a._creationTime < b._creationTime) return -1;
  return 0;
};


/**
 * Removes stale AMIs
 *
 * @param {int} minToKeep the minimum number of AMIs to keep, irrespective of maxDays
 * @param {int} maxToKeep the maximum number of AMIs to keep less than {maxDays} old
 * @param {int} maxDays the cutoff days to discard AMIs
 */
function removeStaleAMIs(minToKeep, maxToKeep, maxDays) {

  if (AWS.config.creditials == null) {
    AWS.config.loadFromPath(__dirname + '/aws-config.json');
  }

  var ec2 = new AWS.EC2();

  ec2.describeImages({Owners: ['self']}, function (err, data) {

    var NAME_LHS = "name=";

    var cutoffTime = moment.utc().subtract(maxDays, 'days').format('YYYY-MM-DD HH:mm:ss [UTC]');

    // convert available images array to an object {imageBuckets} representing a hash map where
    // (k, v) -> (image type, array of images)
    var imageBuckets = data.Images.reduce(function (o, v) {
      var name = null;
      v.Description.split(",").every(function (e) {
        var strim = e.trim();
        if (strim.indexOf(NAME_LHS) === 0) {
          name = strim.substring(NAME_LHS.length, strim.length);
          return false; //return immediately
        }
        return true;
      });
      if (name != null) { // else ignore those without names
        if (o[name]) { o[name].push(v) }
       else { o[name] = [v] }
      }
      return o;
    }, {});

    Object.keys(imageBuckets).forEach(function(e){ // for each type
      var imageType = imageBuckets[e].map(function(el){
        //mutate... add _creationTime to the original object so we don't have to look for it each time
        el._creationTime = el.Tags.filter(function(item){ return (item.Key == "creation_time")})[0].Value;
        return el;
      }).sort(sortByCreationTime);

      var delCount = 0; // delCount == imagesToDelete.length
      var imagesToDelete = imageType.filter(function(el) {
        if (el._creationTime < cutoffTime) { //if anything is out of the cutoff, automatically add it to the list of removals
          delCount++;
          return true;
        } else {
          // we want a max of {maxToKeep} items within the cutoff
          if (imageType.length - delCount > maxToKeep) {
            delCount++;
            return true;
          }
        }
      });
      // enforce minimum condition
      if (imageType.length - imagesToDelete.length < minToKeep) {
        imagesToDelete = imagesToDelete.slice(0, imageType.length - minToKeep);
      }

      imagesToDelete.forEach(function (el) {
        //deregister each el
        ec2.deregisterImage({ImageId: el.ImageId, DryRun: false}, function(err, data) {
          if (err) console.log(err, err.stack); // an error occurred
          else console.log("deregistering: " + el.ImageId);
        });
      });
    });
  });
};

var minToKeep = parseInt(process.argv[2]),
    maxToKeep = parseInt(process.argv[3]),
    maxDays = parseInt(process.argv[4]);

if (process.argv.length == 5 || !(isNaN(minToKeep) || isNaN(maxToKeep) || isNaN(maxDays))) {
  removeStaleAMIs(parseInt(process.argv[2]), parseInt(process.argv[3]), parseInt(process.argv[4])); //TODO: use getopt
} else {
  console.log("improper usage: node remove-stale-ami.js [MIN_AMIS] [MAX_AMIS] [CUTOFF_DAYS]");
}
