package com.example.safeapp;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Random;

/**
 * AdminControls provides an interface for controls that the administrator will use.
 */
public class AdminControls extends AppCompatActivity implements UsernameDialog.UsernameDialogListener,
        CredentialDialog.CredentialDialogListener, RemoveUserDialog.RemoveUserDialogListener,
        RemoveCredentialDialog.RemoveCredentialDialogListener {

    private Button btnNewUser;
    private Button btnAddCredential;
    private Button btnRemoveUser;
    private Button btnRemoveCredential;
    private ListView listUsers;

    DatabaseReference databaseUsers;
    ArrayList<User> users;

    private int MAX_FAIL_LOGIN_ATTEMPTS = 3;

    /**
     * Loads the screen
     * @param savedInstanceState
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_admin_controls);


        // Setup buttons
        btnNewUser = (Button) findViewById(R.id.btnNewUser);
        btnAddCredential = (Button) findViewById(R.id.btnAddCredential);
        btnRemoveUser = (Button) findViewById(R.id.btnRemoveUser);
        btnRemoveCredential = (Button) findViewById(R.id.btnRemoveCredential);
        listUsers = (ListView) findViewById(R.id.listUsers);

        btnNewUser.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                openUsernameDialog();
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

    /**
     * Generates a 4 digit usercode
     * @return 4 digit integer
     */
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

    /**
     * Hashes 4 digit usercode
     * @param passcode 4 digit integer
     * @return String containing hashed value
     */
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

    /**
     * Generates random 4 digit value
     * @return 4 digit integer
     */
    private int randomFourDigitValue() {
        Random r = new Random();
        return r.nextInt((9999-1000) + 1) + 1000;
    }

    /**
     * Adds a credential for a user
     * @param usercode usercode to store
     * @param safe safe number to access
     */
    private void addCredential(int usercode, int safe) {
        int passcode = randomFourDigitValue();
        String hashedPasscode = hashPasscode(passcode);
        Credential credential = new Credential(hashedPasscode, safe);

        if(users.size() == 0) {
            Toast.makeText(this, String.format("Something went wrong, no users found"), Toast.LENGTH_LONG).show();
            return;
        }
        for(User user: users) {
            if(user.getUser_code() == usercode) {
                updateUser(user, credential);
                Toast.makeText(this, String.format("Access safe %s with passcode %s",
                        safe, passcode), Toast.LENGTH_LONG).show();

                return;
            }
        }
        Toast.makeText(this, String.format("User %s was not found", usercode), Toast.LENGTH_LONG).show();
    }

    /**
     * Updates a user with a credential
     * @param user user to update
     * @param credential credential to add
     */
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

    /**
     * Opens UsernameDialog
     */
    private void openUsernameDialog() {
        UsernameDialog usernameDialog = new UsernameDialog(this);
        usernameDialog.show(getSupportFragmentManager(), "Username dialog");
    }

    /**
     * Opens CredentialDialog
     */
    private void openCredentialDialog() {
        CredentialDialog credentialDialog = new CredentialDialog(this);
        credentialDialog.show(getSupportFragmentManager(), "Credential dialog");
    }

    /**
     * Opens RemoveUserDialog
     */
    private void openRemoveUserDialog() {
        RemoveUserDialog removeUserDialog = new RemoveUserDialog(this);
        removeUserDialog.show(getSupportFragmentManager(), "Remove user dialog");
    }

    /**
     * Opens RemoveCredentialDialog
     */
    private void openRemoveCredentialDialog() {
        RemoveCredentialDialog removeCredentialDialog = new RemoveCredentialDialog(this);
        removeCredentialDialog.show(getSupportFragmentManager(), "Remove credential dialog");
    }

    /**
     * Opens AlertDialog
     */
    private void openUserFailedAlertDialog(int usercode) {
        AlertDialog alertDialog = new AlertDialog(String.format("User %s failed to login 3 times", usercode));
        alertDialog.show(getSupportFragmentManager(), "Alert dialog");
    }


    /**
     * Adds a new user
     * @param username username to add
     */
    @Override
    public void applyNewUsername(String username) {
        addNewUser(username);
    }

    /**
     * Adds a new credential
     * @param usercode usercode to update
     * @param safenumber safe to update
     */
    @Override
    public void applyNewCredential(int usercode, int safenumber) {
        addCredential(usercode, safenumber);
    }

    /**
     * Removes a user
     * @param usercode user to remove
     */
    @Override
    public void applyRemoveUser(int usercode) {
        removeUser(usercode);
    }

    /**
     * Removes a credential
     * @param usercode user to remove credential for
     * @param safenumber safe to remove access to
     */
    @Override
    public void applyRemoveCredential(int usercode, int safenumber) {
        removeCredential(usercode, safenumber);
    }

    /**
     * Removes credential for safe number
     * @param usercode user to remove credential for
     * @param safenumber safe to remove access to
     */
    private void removeCredential(int usercode, int safenumber) {
        if(users.size() == 0) {
            Toast.makeText(this, String.format("Something went wrong, no users found"), Toast.LENGTH_LONG).show();
            return;
        }
        for(User user: users) {
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
                Toast.makeText(this, String.format("Credential for user %s was not found", usercode), Toast.LENGTH_LONG).show();
            }
        }
        Toast.makeText(this, String.format("User %s was not found", usercode), Toast.LENGTH_LONG).show();
    }

    /**
     * Removes a user
     * @param usercode user to remove
     */
    private void removeUser(int usercode) {
        if(users.size() == 0) {
            Toast.makeText(this, String.format("Something went wrong, no users found"), Toast.LENGTH_LONG).show();
            return;
        }
        for(User user: users) {
            if(user.getUser_code() == usercode) {
                databaseUsers.child(user.getFirebase_id()).removeValue();
                Toast.makeText(this, String.format("User %s was removed", usercode), Toast.LENGTH_LONG).show();
                return;
            }
        }
        Toast.makeText(this, String.format("User %s was not found", usercode), Toast.LENGTH_LONG).show();
    }

    /**
     * Adds a new user
     * @param username user to add
     */
    private void addNewUser(String username) {
        String id = databaseUsers.push().getKey();
        int usercode = generateNewUsercode();

        User user = new User(username, usercode, new ArrayList<Credential>(), id);
        databaseUsers.child(id).setValue(user);
        Toast.makeText(this, String.format("User %s has been added with usercode %s",
                username, usercode), Toast.LENGTH_LONG).show();
    }

    /**
     * Checks for failed login attempts
     */
    private void checkForFailedLogins() {
        for (User user: users) {
            if (user.getCredentials() != null) {
                for (Credential c: user.getCredentials()) {
                    if (c.getFailed_login_count() >= MAX_FAIL_LOGIN_ATTEMPTS) {
                        openUserFailedAlertDialog(user.getUser_code());

                        c.resetLoginCount();
                        databaseUsers.child(user.getFirebase_id()).setValue(user);
                    }
                }
            }
        }
    }

    /**
     * Loads firebase database
     */
    private void loadUserDatabase() {
        databaseUsers.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                users.clear();

                for(DataSnapshot postSnapshot : dataSnapshot.getChildren()) {
                    User user = postSnapshot.getValue(User.class);
                    users.add(user);
                }

                UserList userList = new UserList(AdminControls.this, users);
                listUsers.setAdapter(userList);
                checkForFailedLogins();
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }
}
