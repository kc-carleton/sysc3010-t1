package com.example.safeapp;

/**
 * Credential defines the properties of a safe credential
 */
public class Credential {

    private String hashed_passcode;
    private int safe;
    private int failed_login_count;

    public Credential() {

    }

    public Credential(String hashed_passcode, int safe) {
        this.hashed_passcode = hashed_passcode;
        this.safe = safe;
        this.failed_login_count = 0;
    }

    public String getHashed_passcode() {
        return hashed_passcode;
    }

    public int getSafe() {
        return safe;
    }

    public void resetLoginCount() {
        this.failed_login_count = 0;
    }

    public int getFailed_login_count() {
        return failed_login_count;
    }
}
