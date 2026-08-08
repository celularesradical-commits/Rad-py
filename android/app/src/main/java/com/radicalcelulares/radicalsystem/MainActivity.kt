package com.radicalcelulares.radicalsystem

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast

class MainActivity : Activity() {

    private lateinit var webView: WebView

    private var pedidoCameraPendente: PermissionRequest? = null

    private val CAMERA_PERMISSION_CODE = 1001
    private val BLUETOOTH_PERMISSION_CODE = 1002

    private val RADICAL_URL =
        "https://radicalsystem.streamlit.app"

    private val PREFS = "radicalsystem_config"
    private val PREF_IMPRESSORA = "impressora_mac"

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

        webView.webViewClient = object : WebViewClient() {

            override fun shouldOverrideUrlLoading(
                view: WebView?,
                request: WebResourceRequest?
            ): Boolean {

                val url = request?.url?.toString()
                    ?: return false

                // Detecta comando vindo do Streamlit
                if (
                    url.contains(
                        "configurar_impressora=1"
                    )
                ) {

                    abrirConfiguracaoImpressora()

                    return true
                }

                return false
            }
        }

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

            webView.loadUrl(
                RADICAL_URL
            )
        }
    }

    // =========================
    // CONFIGURAR IMPRESSORA
    // =========================

    private fun abrirConfiguracaoImpressora() {

        if (
            Build.VERSION.SDK_INT >= Build.VERSION_CODES.S &&
            checkSelfPermission(
                Manifest.permission.BLUETOOTH_CONNECT
            ) != PackageManager.PERMISSION_GRANTED
        ) {

            requestPermissions(
                arrayOf(
                    Manifest.permission.BLUETOOTH_CONNECT
                ),
                BLUETOOTH_PERMISSION_CODE
            )

            return
        }

        mostrarImpressorasPareadas()
    }

    // =========================
    // LISTAR IMPRESSORAS
    // =========================

    private fun mostrarImpressorasPareadas() {

        try {

            val bluetoothManager =
                getSystemService(
                    Context.BLUETOOTH_SERVICE
                ) as BluetoothManager

            val bluetoothAdapter =
                bluetoothManager.adapter

            if (bluetoothAdapter == null) {

                Toast.makeText(
                    this,
                    "Bluetooth não disponível neste aparelho.",
                    Toast.LENGTH_LONG
                ).show()

                return
            }

            if (!bluetoothAdapter.isEnabled) {

                Toast.makeText(
                    this,
                    "Ative o Bluetooth do celular primeiro.",
                    Toast.LENGTH_LONG
                ).show()

                return
            }

            val dispositivos =
                bluetoothAdapter.bondedDevices
                    .toList()
                    .sortedBy {
                        it.name ?: ""
                    }

            if (dispositivos.isEmpty()) {

                Toast.makeText(
                    this,
                    "Nenhum dispositivo Bluetooth pareado.",
                    Toast.LENGTH_LONG
                ).show()

                return
            }

            val nomes =
                dispositivos.map {

                    val nome =
                        it.name ?: "Dispositivo Bluetooth"

                    "$nome\n${it.address}"

                }.toTypedArray()

            AlertDialog.Builder(this)
                .setTitle(
                    "Selecionar impressora"
                )
                .setItems(
                    nomes
                ) { _, posicao ->

                    val dispositivo =
                        dispositivos[posicao]

                    salvarImpressora(
                        dispositivo.address
                    )

                    Toast.makeText(
                        this,
                        "Impressora selecionada: ${
                            dispositivo.name
                                ?: dispositivo.address
                        }",
                        Toast.LENGTH_LONG
                    ).show()
                }
                .setNegativeButton(
                    "Cancelar",
                    null
                )
                .show()

        } catch (erro: Exception) {

            Toast.makeText(
                this,
                "Erro ao acessar Bluetooth: ${erro.message}",
                Toast.LENGTH_LONG
            ).show()
        }
    }

    // =========================
    // SALVAR IMPRESSORA
    // =========================

    private fun salvarImpressora(
        mac: String
    ) {

        getSharedPreferences(
            PREFS,
            Context.MODE_PRIVATE
        )
            .edit()
            .putString(
                PREF_IMPRESSORA,
                mac
            )
            .apply()
    }

    // =========================
    // PERMISSÕES
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

        // -------------------------
        // Câmera
        // -------------------------

        if (
            requestCode ==
            CAMERA_PERMISSION_CODE
        ) {

            val pedido =
                pedidoCameraPendente

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

        // -------------------------
        // Bluetooth
        // -------------------------

        if (
            requestCode ==
            BLUETOOTH_PERMISSION_CODE
        ) {

            if (
                grantResults.isNotEmpty() &&
                grantResults[0] ==
                PackageManager.PERMISSION_GRANTED
            ) {

                mostrarImpressorasPareadas()

            } else {

                Toast.makeText(
                    this,
                    "Permissão Bluetooth necessária para configurar a impressora.",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }

    // =========================
    // BOTÃO VOLTAR
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

        webView.saveState(
            outState
        )

        super.onSaveInstanceState(
            outState
        )
    }
}