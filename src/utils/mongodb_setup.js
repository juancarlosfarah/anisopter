// Set up indexes.
db.spikes.ensureIndex({"sample_id": -1, "_id": 1});
db.frames.ensureIndex({"sample_id": -1, "_id": 1});

// Test sample for CSTMD1.
for (var i = 0; i < 20; i++) {
    frame = []; for (var j = 0; j < 4096; j++) {
        frame[j] = 0;
    }
    db.frames.insert({
        "simulation_id": ObjectId("552d618629750413075fde0d"),
        "frame": frame
    });
}