package com.example.safeapp;

import java.util.ArrayList;

public class User {

    private String user_name;
    private int user_code;
    private ArrayList<Credential> credentials;
    private String firebase_id;

    public User() {

    }

    public User(String user_name, int user_code, ArrayList<Credential> credentials, String firebase_id) {
        this.user_name = user_name;
        this.user_code = user_code;
        this.credentials = credentials;
        this.firebase_id = firebase_id;
    }

    public void setCredentials(ArrayList<Credential> credentials) {
        this.credentials = credentials;
    }

    public int getUser_code() {
        return user_code;
    }

    public String getUser_name() {
        return user_name;
    }

    public ArrayList<Credential> getCredentials() {
        return credentials;
    }

    public String getFirebase_id() {
        return firebase_id;
    }
}
