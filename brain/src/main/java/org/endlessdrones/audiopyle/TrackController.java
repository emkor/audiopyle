package org.endlessdrones.audiopyle;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;


@Controller
@RequestMapping(path = "/track")
public class TrackController {
    @Autowired
    private TrackRepository trackRepository;

    @RequestMapping(method = RequestMethod.POST)
    public @ResponseBody
    ResponseEntity<Track> addTrack(@RequestBody Track new_track) {
        trackRepository.save(new_track);
        return new ResponseEntity<Track>(new_track, HttpStatus.CREATED);
    }

    @RequestMapping(method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<Iterable<Track>> listTracks() {
        return new ResponseEntity<Iterable<Track>>(trackRepository.findAll(), HttpStatus.OK);
    }
}