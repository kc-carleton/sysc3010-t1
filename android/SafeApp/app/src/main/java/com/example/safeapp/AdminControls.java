package com.example.safeapp;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Random;

public class AdminControls extends AppCompatActivity implements UsernameDialog.UsernameDialogListener,
        CredentialDialog.CredentialDialogListener, RemoveUserDialog.RemoveUserDialogListener,
        RemoveCredentialDialog.RemoveCredentialDialogListener {

    private Button btnNewUser;
    private Button btnDisplayDatabase;
    private Button btnAddCredential;
    private Button btnRemoveUser;
    private Button btnRemoveCredential;

    DatabaseReference databaseUsers;
    ArrayList<User> users;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_admin_controls);


        // Setup buttons
        btnNewUser = (Button) findViewById(R.id.btnNewUser);
        btnDisplayDatabase = (Button) findViewById(R.id.btnDisplayDataBase);
        btnAddCredential = (Button) findViewById(R.id.btnAddCredential);
        btnRemoveUser = (Button) findViewById(R.id.btnRemoveUser);
        btnRemoveCredential = (Button) findViewById(R.id.btnRemoveCredential);

        btnNewUser.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openUsernameDialog();
            }
        });
        btnDisplayDatabase.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                displayDatabase();
            }
        });
        btnAddCredential.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openCredentialDialog();
            }
        });
        btnRemoveUser.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openRemoveUserDialog();
            }
        });
        btnRemoveCredential.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openRemoveCredentialDialog();
            }
        });

        // Load database
        databaseUsers = FirebaseDatabase.getInstance().getReference("users");
        users = new ArrayList<>();
        loadUserDatabase();
    }

    private int generateNewUsercode() {
        ArrayList<Integer> existingUsercodes = new ArrayList<>();
        for(User user: users) {
            existingUsercodes.add(user.getUser_code());
        }
        int newUsercode = randomFourDigitValue();
        while(existingUsercodes.contains(newUsercode)) {
            newUsercode = randomFourDigitValue();
        }

        return newUsercode;
    }

    private String hashPasscode(int passcode) {
        try{
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(Integer.toString(passcode).getBytes("UTF-8"));
            StringBuffer hexString = new StringBuffer();

            for (int i = 0; i < hash.length; i++) {
                String hex = Integer.toHexString(0xff & hash[i]);
                if(hex.length() == 1) hexString.append('0');
                hexString.append(hex);
            }

            return hexString.toString();
        } catch(Exception ex){
            throw new RuntimeException(ex);
        }
    }

    private int randomFourDigitValue() {
        Random r = new Random();
        return r.nextInt((9999-1000) + 1) + 1000;
    }

    private void addCredential(int usercode, int safe) {
        int passcode = randomFourDigitValue();
        String hashedPasscode = hashPasscode(passcode);
        System.out.println("Hashed passcode: " + hashedPasscode);
        Credential credential = new Credential(hashedPasscode, safe);

        if(users.size() == 0) {
            Toast.makeText(this, String.format("Something went wrong, no users found"), Toast.LENGTH_LONG).show();
            System.out.println("ERROR: 0 users in database for credential");
            return;
        }
        for(User user: users) {
            System.out.println(user.getUser_name());
            if(user.getUser_code() == usercode) {
                updateUser(user, credential);
                Toast.makeText(this, String.format("Access safe %s with passcode %s",
                        safe, passcode), Toast.LENGTH_LONG).show();

                return;
            }
        }
        Toast.makeText(this, String.format("User %s was not found", usercode), Toast.LENGTH_LONG).show();
        System.out.println(String.format("User %s was not found", usercode));
    }

    private void updateUser(User user, Credential credential) {
        ArrayList<Credential> existingCredentials = user.getCredentials();
        if(existingCredentials == null) {
            existingCredentials = new ArrayList<>();
        } else {
            for (Credential c : existingCredentials) {
                if(c.getSafe() == credential.getSafe()) {
                    Toast.makeText(this, String.format("Safe %s already exists for user %s",
                            credential.getSafe(), user.getUser_code()), Toast.LENGTH_LONG).show();
                    return;
                }
            }
        }
        existingCredentials.add(credential);
        user.setCredentials(existingCredentials);
        databaseUsers.child(user.getFirebase_id()).setValue(user);
    }

    private void displayDatabase() {
        // TODO:
    }

    private void openUsernameDialog() {
        UsernameDialog usernameDialog = new UsernameDialog();
        usernameDialog.show(getSupportFragmentManager(), "Username dialog");
    }

    private void openCredentialDialog() {
        CredentialDialog credentialDialog = new CredentialDialog(this);
        credentialDialog.show(getSupportFragmentManager(), "Credential dialog");
    }

    private void openRemoveUserDialog() {
        RemoveUserDialog removeUserDialog = new RemoveUserDialog(this);
        removeUserDialog.show(getSupportFragmentManager(), "Remove user dialog");
    }

    private void openRemoveCredentialDialog() {
        RemoveCredentialDialog removeCredentialDialog = new RemoveCredentialDialog(this);
        removeCredentialDialog.show(getSupportFragmentManager(), "Remove credential dialog");
    }


    @Override
    public void applyNewUsername(String username) {
        addNewUser(username);
    }

    @Override
    public void applyNewCredential(int usercode, int safenumber) {
        addCredential(usercode, safenumber);
    }

    @Override
    public void applyRemoveUser(int usercode) {
        removeUser(usercode);
    }

    @Override
    public void applyRemoveCredential(int usercode, int safenumber) {
        removeCredential(usercode, safenumber);
    }

    private void removeCredential(int usercode, int safenumber) {
        if(users.size() == 0) {
            Toast.makeText(this, String.format("Something went wrong, no users found"), Toast.LENGTH_LONG).show();
            System.out.println("ERROR: 0 users in database for credential");
            return;
        }
        for(User user: users) {
            System.out.println(user.getUser_name());
            if(user.getUser_code() == usercode) {
                ArrayList<Credential> credentials = user.getCredentials();
                if(credentials != null && credentials.size() > 0) {
                    Credential credentialToRemove = null;
                    for(Credential c: credentials) {
                        if(c.getSafe() == safenumber) {
                            credentialToRemove = c;
                            break;
                        }
                    }
                    if(credentialToRemove != null) {
                        credentials.remove(credentialToRemove);
                        user.setCredentials(credentials);
                        databaseUsers.child(user.getFirebase_id()).setValue(user);
                        Toast.makeText(this, String.format("Safe %s removed", safenumber), Toast.LENGTH_LONG).show();
                        return;
                    }
                }
            }
        }
        Toast.makeText(this, String.format("User %s was not found", usercode), Toast.LENGTH_LONG).show();
        System.out.println(String.format("User %s was not found", usercode));
    }

    private void removeUser(int usercode) {
        if(users.size() == 0) {
            Toast.makeText(this, String.format("Something went wrong, no users found"), Toast.LENGTH_LONG).show();
            System.out.println("ERROR: 0 users in database for credential");
            return;
        }
        for(User user: users) {
            System.out.println(user.getUser_name());
            if(user.getUser_code() == usercode) {
                databaseUsers.child(user.getFirebase_id()).removeValue();
                Toast.makeText(this, String.format("User %s was removed", usercode), Toast.LENGTH_LONG).show();
                System.out.println(String.format("User %s was removed", usercode));
                return;
            }
        }
        Toast.makeText(this, String.format("User %s was not found", usercode), Toast.LENGTH_LONG).show();
        System.out.println(String.format("User %s was not found", usercode));
    }

    private void addNewUser(String username) {
        String id = databaseUsers.push().getKey();
        int usercode = generateNewUsercode();

        User user = new User(username, usercode, new ArrayList<Credential>(), id);
        System.out.println(id + " " + databaseUsers.toString());
        databaseUsers.child(id).setValue(user);
        Toast.makeText(this, String.format("User %s has been added with usercode %s",
                username, usercode), Toast.LENGTH_LONG).show();
    }

    private void loadUserDatabase() {
        databaseUsers.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                users.clear();
                System.out.println("Reloading user data");
                for(DataSnapshot postSnapshot : dataSnapshot.getChildren()) {
                    User user = postSnapshot.getValue(User.class);
                    users.add(user);
                    System.out.println("User has been found: " + user.getUser_name());
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {
                System.out.println("ERROR: Database failed to load");
            }
        });
    }
}