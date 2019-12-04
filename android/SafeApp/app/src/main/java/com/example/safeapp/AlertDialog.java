package com.example.safeapp;

import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatDialogFragment;

/**
 * AlertDialog displays a dialog
 */
public class AlertDialog extends AppCompatDialogFragment {

    private TextView txtAlert;
    private String text;

    public AlertDialog(String text) {
        this.text = text;
    }

    /**
     * Creates the dialog
     * @param savedInstanceState
     * @return built dialog
     */
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(getActivity());

        LayoutInflater inflator = getActivity().getLayoutInflater();
        View view = inflator.inflate(R.layout.layout_alert, null);
        txtAlert = view.findViewById(R.id.txtAlert);
        txtAlert.setText(text);

        builder.setView(view)
                .setTitle("Alert!")
                .setPositiveButton("ok", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        return;
                    }
                });
        return builder.create();
    }
}
