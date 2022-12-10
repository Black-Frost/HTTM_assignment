package com.lampa.emotionrecognition;

import android.graphics.Bitmap;
import android.graphics.Rect;

import java.util.List;

interface DrawBorderCallback {
    public void exec(Bitmap imageBitmap, List<Rect> faces);
}
