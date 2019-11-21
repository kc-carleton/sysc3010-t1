package com.example.safeapp;

public class Credential {

    private String hashed_passcode;
    private int safe;
    private int failedLoginCount;

    public Credential() {

    }

    public Credential(String hashed_passcode, int safe) {
        this.hashed_passcode = hashed_passcode;
        this.safe = safe;
        this.failedLoginCount = 0;
    }

    public String getHashed_passcode() {
        return hashed_passcode;
    }

    public int getSafe() {
        return safe;
    }

    public void resetLoginCount() {
        this.failedLoginCount = 0;
    }

    public int getFailedLoginCount() {
        return failedLoginCount;
    }
}
