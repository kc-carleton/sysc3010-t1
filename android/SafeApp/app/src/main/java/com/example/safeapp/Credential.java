package com.example.safeapp;

public class Credential {

    private String hashed_passcode;
    private int safe;

    public Credential() {

    }

    public Credential(String hashed_passcode, int safe) {
        this.hashed_passcode = hashed_passcode;
        this.safe = safe;
    }

    public String getHashed_passcode() {
        return hashed_passcode;
    }

    public int getSafe() {
        return safe;
    }
}
