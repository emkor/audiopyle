package org.endlessdrones.audiopyle;


import javax.persistence.Id;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;


@Entity
public class Track {

    private
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    Long id;

    private String artistName;
    private String trackName;
    private Double lengthSeconds;

    public String getArtistName() {
        return artistName;
    }

    public void setArtistName(String artistName) {
        this.artistName = artistName;
    }

    public String getTrackName() {
        return trackName;
    }

    public void setTrackName(String trackName) {
        this.trackName = trackName;
    }

    public Double getLengthSeconds() {
        return lengthSeconds;
    }

    public void setLengthSeconds(Double lengthSeconds) {
        this.lengthSeconds = lengthSeconds;
    }
}