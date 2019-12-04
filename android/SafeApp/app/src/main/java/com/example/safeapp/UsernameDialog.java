package com.example.safeapp;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatDialogFragment;

/**
 * UsernameDialog displays a dialog
 */
public class UsernameDialog extends AppCompatDialogFragment {
    private EditText editTextUsername;
    private UsernameDialogListener listener;
    private AdminControls callerClass;

    public UsernameDialog(AdminControls callerClass) {
        this.callerClass = callerClass;
    }

    /**
     * Attaches the listener for the class
     * @param context
     */
    @Override
    public void onAttach(Context context) {
        super.onAttach(context);

        try {
            listener = (UsernameDialogListener) context;
        } catch (ClassCastException e) {
            throw new ClassCastException(context.toString() + "must implement UsernameDialogListener");
        }
    }

    /**
     * Creates the dialog
     * @param savedInstanceState
     * @return built dialog
     */
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());

        LayoutInflater inflator = getActivity().getLayoutInflater();
        View view = inflator.inflate(R.layout.layout_dialog, null);
        editTextUsername = view.findViewById(R.id.editUsername);

        builder.setView(view)
                .setTitle("Create username")
                .setNegativeButton("cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                    }
                })
                .setPositiveButton("ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String username = editTextUsername.getText().toString();
                        if (username.contains("\n")) {
                            Toast.makeText(callerClass, String.format("Your username must be a string"), Toast.LENGTH_LONG).show();
                            return;
                        }
                        listener.applyNewUsername(username);
                    }
                });
        return builder.create();
    }

    /**
     * Applies the dialog operation
     */
    public interface UsernameDialogListener {
        void applyNewUsername(String username);
    }
}
