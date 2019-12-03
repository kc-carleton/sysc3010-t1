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
 * RemoveUserDialog displays a dialog
 */
public class RemoveUserDialog extends AppCompatDialogFragment {
    private EditText editTextUsercode;
    private RemoveUserDialog.RemoveUserDialogListener listener;
    private AdminControls callerClass;

    public RemoveUserDialog(AdminControls callerClass) {
        this.callerClass = callerClass;
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
        View view = inflator.inflate(R.layout.layout_remove_user, null);
        editTextUsercode = view.findViewById(R.id.editUsercode);

        builder.setView(view)
                .setTitle("Input usercode to remove")
                .setNegativeButton("cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                    }
                })
                .setPositiveButton("ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        int usercode;
                        try {
                            usercode = Integer.parseInt(editTextUsercode.getText().toString());
                            if(usercode < 1000 || usercode > 9999) {
                                throw new Exception("code not valid");
                            }
                        } catch (Exception e) {
                            Toast.makeText(callerClass, String.format("You must provide usercode as 4 digit integer"), Toast.LENGTH_LONG).show();
                            System.out.println("ERROR: You must provide usercode as 4 digit integer");
                            return;
                        }

                        listener.applyRemoveUser(usercode);
                    }
                });
        return builder.create();
    }

    /**
     * Attaches the listener for the class
     * @param context
     */
    @Override
    public void onAttach(Context context) {
        super.onAttach(context);

        try {
            listener = (RemoveUserDialog.RemoveUserDialogListener) context;
        } catch (ClassCastException e) {
            throw new ClassCastException(context.toString() + "must implement RemoveUserDialogListener");
        }
    }

    /**
     * Applies the dialog operation
     */
    public interface RemoveUserDialogListener {
        void applyRemoveUser(int usercode);
    }
}
