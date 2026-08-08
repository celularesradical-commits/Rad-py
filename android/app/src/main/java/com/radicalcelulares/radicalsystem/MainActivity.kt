package com.radicalcelulares.radicalsystem

import android.Manifest
import android.app.Activity
import android.content.pm.PackageManager
import android.os.Bundle
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient

class MainActivity : Activity() {

    private lateinit var webView: WebView

    private var pedidoCameraPendente: PermissionRequest? = null

    private val CAMERA_PERMISSION_CODE = 1001

    private val RADICAL_URL =
        "https://radicalsystem.streamlit.app"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)

        setContentView(webView)

        // =========================
        // CONFIGURAÇÃO DO WEBVIEW
        // =========================

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true

        webView.settings.allowFileAccess = false
        webView.settings.allowContentAccess = false

        webView.webViewClient = WebViewClient()

        // =========================
        // CÂMERA
        // =========================

        webView.webChromeClient = object : WebChromeClient() {

            override fun onPermissionRequest(
                request: PermissionRequest
            ) {

                runOnUiThread {

                    val origemPermitida =
                        request.origin.host ==
                        "radicalsystem.streamlit.app"

                    val pediuCamera =
                        request.resources.contains(
                            PermissionRequest.RESOURCE_VIDEO_CAPTURE
                        )

                    if (!origemPermitida || !pediuCamera) {
                        request.deny()
                        return@runOnUiThread
                    }

                    if (
                        checkSelfPermission(
                            Manifest.permission.CAMERA
                        ) == PackageManager.PERMISSION_GRANTED
                    ) {

                        request.grant(
                            arrayOf(
                                PermissionRequest.RESOURCE_VIDEO_CAPTURE
                            )
                        )

                    } else {

                        pedidoCameraPendente = request

                        requestPermissions(
                            arrayOf(
                                Manifest.permission.CAMERA
                            ),
                            CAMERA_PERMISSION_CODE
                        )
                    }
                }
            }
        }

        // =========================
        // ABRIR RADICALSYSTEM
        // =========================

        if (savedInstanceState == null) {
            webView.loadUrl(RADICAL_URL)
        }
    }

    // =========================
    // RESPOSTA DA PERMISSÃO
    // =========================

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {

        super.onRequestPermissionsResult(
            requestCode,
            permissions,
            grantResults
        )

        if (requestCode == CAMERA_PERMISSION_CODE) {

            val pedido = pedidoCameraPendente

            if (
                grantResults.isNotEmpty() &&
                grantResults[0] ==
                PackageManager.PERMISSION_GRANTED
            ) {

                pedido?.grant(
                    arrayOf(
                        PermissionRequest.RESOURCE_VIDEO_CAPTURE
                    )
                )

            } else {

                pedido?.deny()
            }

            pedidoCameraPendente = null
        }
    }

    // =========================
    // BOTÃO VOLTAR DO ANDROID
    // =========================

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {

        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }

    // =========================
    // SALVAR ESTADO
    // =========================

    override fun onSaveInstanceState(
        outState: Bundle
    ) {

        webView.saveState(outState)

        super.onSaveInstanceState(outState)
    }
}