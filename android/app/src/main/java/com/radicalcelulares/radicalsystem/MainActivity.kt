package com.radicalcelulares.radicalsystem

import android.Manifest
import android.app.Activity
import android.app.AlertDialog
import android.bluetooth.BluetoothManager
import android.content.Context
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.webkit.CookieManager
import android.webkit.PermissionRequest
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import java.util.UUID
import kotlin.concurrent.thread

class MainActivity : Activity() {

    private lateinit var webView: WebView

    private var pedidoCameraPendente: PermissionRequest? = null
    private var acaoBluetoothPendente: String? = null

    private val CAMERA_PERMISSION_CODE = 1001
    private val BLUETOOTH_PERMISSION_CODE = 1002

    private val RADICAL_URL =
        "https://radicalsystem.streamlit.app"

    private val PREFS = "radicalsystem_config"
    private val PREF_IMPRESSORA = "impressora_mac"

    private val UUID_SPP: UUID =
        UUID.fromString(
            "00001101-0000-1000-8000-00805F9B34FB"
        )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        webView = WebView(this)
        setContentView(webView)

        // =========================
        // CONFIGURAÇÕES WEBVIEW
        // =========================

        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true

        webView.settings.allowFileAccess = false
        webView.settings.allowContentAccess = false

        // Não permitir múltiplas janelas
        webView.settings.javaScriptCanOpenWindowsAutomatically = false
        webView.settings.setSupportMultipleWindows(false)

        // =========================
        // COOKIES / SESSÃO
        // =========================

        val cookieManager =
            CookieManager.getInstance()

        cookieManager.setAcceptCookie(true)

        if (
            Build.VERSION.SDK_INT >=
            Build.VERSION_CODES.LOLLIPOP
        ) {

            cookieManager.setAcceptThirdPartyCookies(
                webView,
                true
            )
        }

        // =========================
        // INTERCEPTAR COMANDOS
        // =========================

        webView.webViewClient =
            object : WebViewClient() {

                // Android moderno
                override fun shouldOverrideUrlLoading(
                    view: WebView?,
                    request: WebResourceRequest?
                ): Boolean {

                    val url =
                        request?.url?.toString()
                            ?: return false

                    return processarUrl(url)
                }

                // Compatibilidade / links disparados pelo Streamlit
                @Deprecated("Deprecated in Java")
                override fun shouldOverrideUrlLoading(
                    view: WebView?,
                    url: String?
                ): Boolean {

                    if (url.isNullOrBlank()) {
                        return false
                    }

                    return processarUrl(url)
                }
            }

        // =========================
        // CÂMERA
        // =========================

        webView.webChromeClient =
            object : WebChromeClient() {

                override fun onPermissionRequest(
                    request: PermissionRequest
                ) {

                    runOnUiThread {

                        val origemPermitida =
                            request.origin.host ==
                                    "radicalsystem.streamlit.app"

                        val pediuCamera =
                            request.resources.contains(
                                PermissionRequest
                                    .RESOURCE_VIDEO_CAPTURE
                            )

                        if (
                            !origemPermitida ||
                            !pediuCamera
                        ) {

                            request.deny()

                            return@runOnUiThread
                        }

                        if (
                            checkSelfPermission(
                                Manifest.permission.CAMERA
                            ) ==
                            PackageManager.PERMISSION_GRANTED
                        ) {

                            request.grant(
                                arrayOf(
                                    PermissionRequest
                                        .RESOURCE_VIDEO_CAPTURE
                                )
                            )

                        } else {

                            pedidoCameraPendente =
                                request

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
        // ABRIR SISTEMA
        // =========================

        if (savedInstanceState == null) {

            webView.loadUrl(
                RADICAL_URL
            )

        } else {

            webView.restoreState(
                savedInstanceState
            )
        }
    }

    // =========================
    // PROCESSAR URL
    // =========================

    private fun processarUrl(
        url: String
    ): Boolean {

        if (
            !url.startsWith(
                "radicalsystem:",
                ignoreCase = true
            )
        ) {

            return false
        }

        try {

            val uri =
                Uri.parse(url)

            /*
             Aceita:

             radicalsystem://configurar-impressora

             radicalsystem:configurar-impressora

             radicalsystem://testar-impressao

             radicalsystem:testar-impressao
             */

            var comando =
                uri.host

            if (comando.isNullOrBlank()) {

                comando =
                    uri.schemeSpecificPart
                        ?.removePrefix("//")
                        ?.substringBefore("?")
                        ?.substringBefore("/")
                        ?.trim()
            }

            comando =
                comando
                    ?.lowercase()
                    ?.trim()

            when (comando) {

                "configurar-impressora" -> {

                    abrirConfiguracaoImpressora()
                }

                "testar-impressao" -> {

                    testarImpressao()
                }

                else -> {

                    mostrarToast(
                        "Comando não reconhecido: $comando"
                    )
                }
            }

        } catch (erro: Exception) {

            mostrarToast(
                "Erro no comando: ${erro.message}"
            )
        }

        return true
    }

    // =========================
    // CONFIGURAR IMPRESSORA
    // =========================

    private fun abrirConfiguracaoImpressora() {

        if (!temPermissaoBluetooth()) {

            acaoBluetoothPendente =
                "configurar"

            pedirPermissaoBluetooth()

            return
        }

        mostrarImpressorasPareadas()
    }

    // =========================
    // PERMISSÃO BLUETOOTH
    // =========================

    private fun temPermissaoBluetooth(): Boolean {

        if (
            Build.VERSION.SDK_INT >=
            Build.VERSION_CODES.S
        ) {

            return checkSelfPermission(
                Manifest.permission
                    .BLUETOOTH_CONNECT
            ) ==
            PackageManager.PERMISSION_GRANTED
        }

        return true
    }

    private fun pedirPermissaoBluetooth() {

        if (
            Build.VERSION.SDK_INT >=
            Build.VERSION_CODES.S
        ) {

            requestPermissions(
                arrayOf(
                    Manifest.permission
                        .BLUETOOTH_CONNECT
                ),
                BLUETOOTH_PERMISSION_CODE
            )

        } else {

            when (
                acaoBluetoothPendente
            ) {

                "configurar" ->
                    mostrarImpressorasPareadas()

                "testar" ->
                    testarImpressao()
            }

            acaoBluetoothPendente = null
        }
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

                mostrarToast(
                    "Bluetooth não disponível neste aparelho."
                )

                return
            }

            if (!bluetoothAdapter.isEnabled) {

                mostrarToast(
                    "Ative o Bluetooth do celular primeiro."
                )

                return
            }

            val dispositivos =
                bluetoothAdapter
                    .bondedDevices
                    .toList()
                    .sortedBy {
                        it.name ?: ""
                    }

            if (dispositivos.isEmpty()) {

                mostrarToast(
                    "Nenhum dispositivo Bluetooth pareado."
                )

                return
            }

            val nomes =
                dispositivos.map {

                    val nome =
                        it.name
                            ?: "Dispositivo Bluetooth"

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

                    mostrarToast(
                        "Impressora selecionada: ${
                            dispositivo.name
                                ?: dispositivo.address
                        }"
                    )
                }
                .setNegativeButton(
                    "Cancelar",
                    null
                )
                .show()

        } catch (erro: Exception) {

            mostrarToast(
                "Erro ao acessar Bluetooth: ${erro.message}"
            )
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
    // TESTAR IMPRESSÃO
    // =========================

    private fun testarImpressao() {

        if (!temPermissaoBluetooth()) {

            acaoBluetoothPendente =
                "testar"

            pedirPermissaoBluetooth()

            return
        }

        val mac =
            getSharedPreferences(
                PREFS,
                Context.MODE_PRIVATE
            )
                .getString(
                    PREF_IMPRESSORA,
                    null
                )

        if (mac.isNullOrBlank()) {

            mostrarToast(
                "Configure uma impressora primeiro."
            )

            return
        }

        mostrarToast(
            "Conectando à impressora..."
        )

        thread {

            var socket:
                    android.bluetooth.BluetoothSocket? =
                null

            try {

                val bluetoothManager =
                    getSystemService(
                        Context.BLUETOOTH_SERVICE
                    ) as BluetoothManager

                val bluetoothAdapter =
                    bluetoothManager.adapter

                if (bluetoothAdapter == null) {

                    mostrarToast(
                        "Bluetooth não disponível."
                    )

                    return@thread
                }

                val dispositivo =
                    bluetoothAdapter
                        .getRemoteDevice(mac)

                bluetoothAdapter
                    .cancelDiscovery()

                socket =
                    dispositivo
                        .createRfcommSocketToServiceRecord(
                            UUID_SPP
                        )

                socket.connect()

                val saida =
                    socket.outputStream

                // Inicializar ESC/POS
                saida.write(
                    byteArrayOf(
                        0x1B,
                        0x40
                    )
                )

                val texto = """
RADICAL CELULARES
------------------------------
TESTE DE IMPRESSAO

RadicalSystem
Impressora configurada!

------------------------------



""".trimIndent()

                saida.write(
                    texto.toByteArray(
                        Charsets.UTF_8
                    )
                )

                saida.flush()

                Thread.sleep(300)

                mostrarToast(
                    "Impressão enviada!"
                )

            } catch (erro: Exception) {

                mostrarToast(
                    "Erro ao imprimir: ${erro.message}"
                )

            } finally {

                try {

                    socket?.close()

                } catch (_: Exception) {
                }
            }
        }
    }

    // =========================
    // TOAST
    // =========================

    private fun mostrarToast(
        mensagem: String
    ) {

        runOnUiThread {

            Toast.makeText(
                this,
                mensagem,
                Toast.LENGTH_LONG
            ).show()
        }
    }

    // =========================
    // RESULTADO DAS PERMISSÕES
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

        // =========================
        // CÂMERA
        // =========================

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
                        PermissionRequest
                            .RESOURCE_VIDEO_CAPTURE
                    )
                )

            } else {

                pedido?.deny()
            }

            pedidoCameraPendente =
                null
        }

        // =========================
        // BLUETOOTH
        // =========================

        if (
            requestCode ==
            BLUETOOTH_PERMISSION_CODE
        ) {

            if (
                grantResults.isNotEmpty() &&
                grantResults[0] ==
                PackageManager.PERMISSION_GRANTED
            ) {

                when (
                    acaoBluetoothPendente
                ) {

                    "configurar" -> {

                        mostrarImpressorasPareadas()
                    }

                    "testar" -> {

                        testarImpressao()
                    }
                }

            } else {

                mostrarToast(
                    "Permissão Bluetooth necessária."
                )
            }

            acaoBluetoothPendente =
                null
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

    // =========================
    // SALVAR COOKIES AO PAUSAR
    // =========================

    override fun onPause() {

        super.onPause()

        CookieManager
            .getInstance()
            .flush()
    }
}