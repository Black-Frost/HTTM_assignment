package com.lampa.emotionrecognition;

import android.graphics.Bitmap;
import android.graphics.Rect;

import java.util.List;
import java.util.Map;

interface DrawBorderCallback {
    public void exec(Bitmap imageBitmap, List<Rect> faces);
}

interface UpdateEmotionListCallback {
    public void exec(List<Map<String, Float>> emotionLists);
}
